"""Download external Kaggle inputs into a shared cache and mount them into a run's kaggle/input.

An input is a "kind:ref" string, as written by triage_static.py in versions.csv (`available_external`):
  dataset:<owner>/<slug>        mounted at kaggle/input/<slug>
  kernel:<owner>/<slug>         (the kernel's output files) mounted at kaggle/input/<slug>
  competition:<slug>            mounted at kaggle/input/<slug>
Models (model:...) are not supported yet.

Cache layout: <cache>/<kind>/<ref>/files/... plus <cache>/<kind>/<ref>/meta.json once complete. Downloads go to a
temporary directory and are renamed into place, so a crash never leaves a half-filled entry. Several runs may ask
for the same input at once; a per-input file lock makes the second one wait and reuse the first download.

Datasets and competitions: the size is read from the response header before writing anything, and the stream has a
hard wall-clock deadline (the kaggle client has no total timeout). Kernel outputs use the kaggle client as-is.

Limitation: this downloads the *current* version of a dataset or kernel output, which may differ from the version
the expert's notebook used.
"""

import fcntl
import json
import os
import shutil
import stat
import time
import zipfile
from pathlib import Path

CHUNK = 1 << 20


class InputError(Exception):
    """Raised with a short status: INPUT_TOO_LARGE, INPUT_DOWNLOAD_FAILED or INPUT_UNSUPPORTED."""

    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


def _api():
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    api.authenticate()
    return api


def parse(spec):
    kind, _, ref = spec.partition(":")
    if kind not in ("dataset", "kernel", "competition", "model") or not ref:
        raise ValueError(f"bad input spec {spec!r}; expected dataset:/kernel:/competition:<ref>")
    folder = ref.split("/")[1] if kind == "model" else ref.split("/")[-1]
    return kind, ref, folder


def _stream_zip(response, out_zip, max_bytes, deadline_s):
    size = int(response.headers.get("Content-Length") or 0)
    if max_bytes and size > max_bytes:
        response.close()
        raise InputError("INPUT_TOO_LARGE", f"{size / 1e9:.1f} GB > limit {max_bytes / 1e9:.1f} GB")
    t0, written = time.time(), 0
    with open(out_zip, "wb") as fh:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            fh.write(chunk)
            written += len(chunk)
            if max_bytes and written > max_bytes:
                raise InputError("INPUT_TOO_LARGE", f"stream exceeded {max_bytes / 1e9:.1f} GB")
            if time.time() - t0 > deadline_s:
                raise InputError("INPUT_DOWNLOAD_FAILED", f"download exceeded {deadline_s} s ({written / 1e9:.2f} GB)")
    response.close()
    return written


def _download(kind, ref, dest, max_bytes, deadline_s):
    """Fill dest/ with the input's files. Returns the number of bytes downloaded."""
    api = _api()
    timeout = (10, 120)
    if kind in ("dataset", "competition"):
        if kind == "dataset":
            owner, slug = ref.split("/", 1)
            resp = api.datasets_download_with_http_info(owner_slug=owner, dataset_slug=slug, _preload_content=False,
                                                        _request_timeout=timeout)[0]
        else:
            resp = api.competitions_data_download_files_with_http_info(id=ref, _preload_content=False,
                                                                       _request_timeout=timeout)[0]
        if resp.status != 200:
            raise InputError("INPUT_DOWNLOAD_FAILED", f"HTTP {resp.status}")
        zpath = dest.parent / (dest.name + ".zip")
        n = _stream_zip(resp, zpath, max_bytes, deadline_s)
        if zipfile.is_zipfile(zpath):
            with zipfile.ZipFile(zpath) as z:  # zipfile drops absolute paths and ".." components
                z.extractall(dest)
            zpath.unlink()
        else:  # a single non-zipped file
            dest.mkdir(parents=True, exist_ok=True)
            zpath.rename(dest / Path(ref).name)
        return n
    if kind == "kernel":
        dest.mkdir(parents=True, exist_ok=True)
        api.kernels_output(ref, str(dest), force=True, quiet=True)
        return sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
    raise InputError("INPUT_UNSUPPORTED", f"{kind} inputs are not supported yet ({ref})")


def fetch(spec, cache, max_bytes=20e9, deadline_s=3600):
    """Make sure the input is in the cache. Returns (files_dir, info dict)."""
    kind, ref, _ = parse(spec)
    entry = Path(cache) / kind / ref
    entry.parent.mkdir(parents=True, exist_ok=True)
    meta = entry / "meta.json"
    with open(str(entry) + ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if meta.exists():
            info = json.loads(meta.read_text())
            return entry / "files", {**info, "cached": True}
        tmp = Path(str(entry) + f".tmp{os.getpid()}")
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        t0 = time.time()
        try:
            n = _download(kind, ref, tmp / "files", max_bytes, deadline_s)
        except InputError:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        except Exception as e:  # noqa: BLE001 - API / network / unzip errors
            shutil.rmtree(tmp, ignore_errors=True)
            msg = str(e).splitlines()[-1][:200] if "HTTP response body" in str(e) else f"{type(e).__name__}: {e}"[:200]
            raise InputError("INPUT_DOWNLOAD_FAILED", msg) from e
        for p in (tmp / "files").rglob("*"):  # cache is read-only; mounts are hardlinks to it
            if p.is_file():
                p.chmod(stat.S_IRUSR | stat.S_IRGRP)
        info = {"spec": spec, "bytes": n, "download_s": round(time.time() - t0, 1),
                "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        (tmp / "meta.json").write_text(json.dumps(info))
        shutil.rmtree(entry, ignore_errors=True)
        tmp.rename(entry)
        return entry / "files", {**info, "cached": False}


def mount(files_dir, dest):
    """Hardlink (or copy, across filesystems) every cached file into dest/. Returns the number of files."""
    n = 0
    for src in Path(files_dir).rglob("*"):
        out = Path(dest) / src.relative_to(files_dir)
        if src.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(src, out)
        except OSError:
            shutil.copy2(src, out)
            out.chmod(stat.S_IRUSR | stat.S_IRGRP)
        n += 1
    return n
