"""Exact external inputs of expert notebook versions, from Meta Kaggle (no regex guessing, works for 2020-22 comps too).

TraceML's state.parquet gives each (key_id, version_number) its Kaggle KernelVersion id (`version_id`). Meta Kaggle maps it:
  KernelVersionDatasetSources  KernelVersionId -> SourceDatasetVersionId
  DatasetVersions              Id -> DatasetId, VersionNumber, Slug, size
  Datasets + Users             DatasetId -> owner user name
  KernelVersionKernelSources   KernelVersionId -> SourceKernelVersionId (utility scripts, notebook outputs)
  KernelVersions + Kernels     SourceKernelVersionId -> kernel slug, its version number, author
Output: one row per (key_id, version, input) with a kaggle_inputs.py spec: dataset:<owner>/<slug>@<N> or
kernel:<owner>/<slug> (kaggle_inputs.py can only fetch a kernel's *current* output; the version used is in kernel_version).
An input whose dataset is not in Meta Kaggle (private or deleted) gets spec "" and a note.

  python src/resolve_inputs.py --versions 18423958:4,8 53762022:8,9 --out triage/large_delta_inputs.csv
"""
import argparse
import getpass
from pathlib import Path

import pandas as pd

USER_DATA = Path("/data/user_data") / getpass.getuser()


def filtered(csv: Path, col: str, keep: set, usecols: list) -> pd.DataFrame:
    """Rows of a large Meta Kaggle csv whose `col` is in `keep`, read in chunks."""
    parts = [c[c[col].isin(keep)] for c in pd.read_csv(csv, usecols=usecols, chunksize=2_000_000, low_memory=False)]
    return pd.concat(parts) if parts else pd.DataFrame(columns=usecols)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--versions", nargs="+", required=True, help="key_id:v1,v2,... (TraceML version numbers)")
    ap.add_argument("--metakaggle", type=Path, default=USER_DATA / "metakaggle")
    ap.add_argument("--traceml", type=Path, default=USER_DATA / "traceml/hf")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    mk = args.metakaggle

    want = {(k, int(v)) for item in args.versions for k, vs in [item.split(":")] for v in vs.split(",")}
    s = pd.concat(pd.read_parquet(args.traceml / f"data/{x}/state.parquet", columns=["key_id", "version_number", "comp", "version_id"])
                  for x in ("paired", "humans_only"))
    s["key_id"] = s.key_id.astype(str)
    s = s[[(k, int(v)) in want for k, v in zip(s.key_id, s.version_number)]].drop_duplicates(["key_id", "version_number"])
    missing = want - set(zip(s.key_id, s.version_number.astype(int)))
    if missing:
        print(f"[resolve] not in TraceML state: {sorted(missing)}")
    kv = dict(zip(s.version_id.astype("int64"), zip(s.key_id, s.version_number.astype(int), s.comp)))

    dsrc = filtered(mk / "KernelVersionDatasetSources.csv", "KernelVersionId", set(kv), ["KernelVersionId", "SourceDatasetVersionId"])
    ksrc = filtered(mk / "KernelVersionKernelSources.csv", "KernelVersionId", set(kv), ["KernelVersionId", "SourceKernelVersionId"])
    dv = filtered(mk / "DatasetVersions.csv", "Id", set(dsrc.SourceDatasetVersionId),
                  ["Id", "DatasetId", "VersionNumber", "Slug", "CreationDate", "TotalUncompressedBytes"])
    ds = filtered(mk / "Datasets.csv", "Id", set(dv.DatasetId), ["Id", "OwnerUserId", "OwnerOrganizationId", "CurrentDatasetVersionId"])
    kver = filtered(mk / "KernelVersions.csv", "Id", set(ksrc.SourceKernelVersionId), ["Id", "ScriptId", "VersionNumber"])
    kern = filtered(mk / "Kernels.csv", "Id", set(kver.ScriptId), ["Id", "AuthorUserId", "CurrentUrlSlug", "CurrentKernelVersionId"])
    users = filtered(mk / "Users.csv", "Id", set(ds.OwnerUserId.dropna().astype("int64")) | set(kern.AuthorUserId), ["Id", "UserName"])
    uname = dict(zip(users.Id, users.UserName))

    rows = []
    dv_by = dv.set_index("Id")
    ds_by = ds.set_index("Id")
    for r in dsrc.itertuples():
        key, ver, comp = kv[r.KernelVersionId]
        row = {"key_id": key, "version": ver, "comp": comp, "kind": "dataset", "source_version_id": r.SourceDatasetVersionId}
        if r.SourceDatasetVersionId not in dv_by.index:
            rows.append({**row, "spec": "", "note": "dataset version not in Meta Kaggle (private or deleted)"})
            continue
        d = dv_by.loc[r.SourceDatasetVersionId]
        owner = ds_by.loc[d.DatasetId] if d.DatasetId in ds_by.index else None
        user = uname.get(owner.OwnerUserId) if owner is not None and pd.notna(owner.OwnerUserId) else None
        spec = f"dataset:{user}/{d.Slug}@{int(d.VersionNumber)}" if user else ""
        rows.append({**row, "spec": spec, "slug": d.Slug, "dataset_version": int(d.VersionNumber), "created": d.CreationDate,
                     "gb": round((d.TotalUncompressedBytes or 0) / 1e9, 2),
                     "note": "" if user else "owner not found (organization or deleted user)"})
    kv_by = kver.set_index("Id")
    kern_by = kern.set_index("Id")
    for r in ksrc.itertuples():
        key, ver, comp = kv[r.KernelVersionId]
        row = {"key_id": key, "version": ver, "comp": comp, "kind": "kernel", "source_version_id": r.SourceKernelVersionId}
        if r.SourceKernelVersionId not in kv_by.index or kv_by.loc[r.SourceKernelVersionId].ScriptId not in kern_by.index:
            rows.append({**row, "spec": "", "note": "kernel version not in Meta Kaggle (private or deleted)"})
            continue
        k = kv_by.loc[r.SourceKernelVersionId]
        kk = kern_by.loc[k.ScriptId]
        user = uname.get(kk.AuthorUserId)
        current = pd.notna(kk.CurrentKernelVersionId) and int(kk.CurrentKernelVersionId) == int(r.SourceKernelVersionId)
        note = ("author not found" if not user else
                "used version is the kernel's current version (downloadable)" if current else
                "used version is NOT the current one: kaggle_inputs can only fetch the current output")
        rows.append({**row, "spec": f"kernel:{user}/{kk.CurrentUrlSlug}" if user else "", "slug": kk.CurrentUrlSlug,
                     "kernel_version": int(k.VersionNumber) if pd.notna(k.VersionNumber) else None,
                     "kernel_is_current": bool(current), "note": note})
    out = pd.DataFrame(rows).sort_values(["key_id", "version", "kind", "spec"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out, index=False)
    print(out.to_string(index=False, max_colwidth=60))
    no_src = sorted(set(kv.values()) - set(zip(out.key_id, out.version, out.comp))) if len(out) else sorted(kv.values())
    if no_src:
        print(f"[resolve] versions with no dataset/kernel sources in Meta Kaggle: {no_src}")


if __name__ == "__main__":
    main()
