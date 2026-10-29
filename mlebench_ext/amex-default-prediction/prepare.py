"""
Kaggle's AMEX data: train_data.csv (~16 GB, ~5.5M rows = monthly statements, many rows per customer_ID),
train_labels.csv (one row per customer_ID: customer_ID,target), test_data.csv (~33 GB, unlabeled, unused
here) and sample_submission.csv (unused).

The split is made on customers, never across a customer: train_labels.csv (one row per customer) is split
90/10 with train_test_split(test_size=0.1, random_state=0) as in the official MLE-bench entries, then every
statement row of train_data.csv goes to the side of its customer.

Memory: train_data.csv is streamed line by line and each raw line is copied unchanged (byte for byte) to
public/train_data.csv or public/test_data.csv, so RAM stays well under 1 GB and the CSV formatting
(float digits, empty fields) is exactly Kaggle's. customer_ID must be the first column (it is).

public/  train_data.csv, train_labels.csv, test_data.csv (same columns as train_data.csv),
         sample_submission.csv (customer_ID, prediction)
private/ answers.csv (customer_ID, target)

Rows keep their original order in every output file.
"""

import time
from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split

from mlebench.utils import get_logger, read_csv

logger = get_logger(__name__)

ID, TARGET = "customer_ID", "target"
BUFFER = 16 * 1024 * 1024
LOG_EVERY = 1_000_000


def split_rows_by_customer(src: Path, dst_train: Path, dst_test: Path, test_ids: set[bytes]) -> dict:
    """Copy each data line of `src` to dst_test if its customer_ID (first field) is in test_ids, else to
    dst_train. The header goes to both. Returns row counts and the customer IDs seen on each side."""
    seen_train, seen_test = set(), set()
    n_train = n_test = 0
    t0 = time.time()
    with open(src, "rb", buffering=BUFFER) as fin, open(dst_train, "wb", buffering=BUFFER) as ftr, open(
        dst_test, "wb", buffering=BUFFER
    ) as fte:
        header = fin.readline()
        first_col = header.split(b",", 1)[0].strip().lstrip(b"\xef\xbb\xbf").strip(b'"')
        assert first_col == ID.encode(), f"expected {ID} as first column of {src}, got {first_col!r}"
        ftr.write(header)
        fte.write(header)
        for line in fin:
            comma = line.find(b",")
            if comma < 0:
                if line.strip():
                    raise ValueError(f"malformed line in {src}: {line[:80]!r}")
                continue  # blank line
            cid = line[:comma].strip(b'"')
            if cid in test_ids:
                fte.write(line)
                seen_test.add(cid)
                n_test += 1
            else:
                ftr.write(line)
                seen_train.add(cid)
                n_train += 1
            if (n_train + n_test) % LOG_EVERY == 0:
                logger.info(f"{n_train + n_test:,} rows split ({time.time() - t0:.0f}s)")
    logger.info(f"split {n_train + n_test:,} rows in {time.time() - t0:.0f}s")
    return {"n_train": n_train, "n_test": n_test, "seen_train": seen_train, "seen_test": seen_test}


def prepare(raw: Path, public: Path, private: Path):
    labels = read_csv(raw / "train_labels.csv", dtype={ID: str})
    assert labels.columns.tolist() == [ID, TARGET], labels.columns.tolist()
    assert labels[ID].is_unique, "train_labels.csv has duplicate customer_IDs"
    assert set(labels[TARGET].unique()) <= {0, 1}

    _, test_part = train_test_split(labels, test_size=0.1, random_state=0)
    is_test = labels[ID].isin(set(test_part[ID]))
    train_labels = labels[~is_test]  # original order
    answers = labels[is_test]  # original order

    test_ids = {c.encode("ascii") for c in answers[ID]}
    train_ids = {c.encode("ascii") for c in train_labels[ID]}

    stats = split_rows_by_customer(
        raw / "train_data.csv", public / "train_data.csv", public / "test_data.csv", test_ids
    )

    sample_submission = answers[[ID]].copy()
    sample_submission["prediction"] = np.random.RandomState(0).uniform(size=len(sample_submission)).round(6)

    # Checks: every labelled customer has statement rows on exactly its own side, and vice versa.
    assert stats["seen_test"] == test_ids, "test customers in train_data.csv differ from held-out labels"
    assert stats["seen_train"] == train_ids, "train customers in train_data.csv differ from train labels"
    assert stats["seen_train"].isdisjoint(stats["seen_test"])
    assert len(train_labels) + len(answers) == len(labels)
    assert answers[ID].tolist() == sample_submission[ID].tolist()

    train_labels.to_csv(public / "train_labels.csv", index=False)
    sample_submission.to_csv(public / "sample_submission.csv", index=False)
    answers.to_csv(private / "answers.csv", index=False)
    logger.info(
        f"customers: {len(train_labels):,} train / {len(answers):,} test; "
        f"statement rows: {stats['n_train']:,} train / {stats['n_test']:,} test"
    )
