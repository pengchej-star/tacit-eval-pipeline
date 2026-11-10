# Installed as sitecustomize.py in the kaggle-run-gpu venv's site-packages.
# Compatibility shims for 2020-2024 notebooks on our 2026 stack. They only add what the old code expects and change
# nothing for code that does not use it. The same venv is mounted in the agent's container, so expert versions and
# agent versions see the same shims.
import importlib.abc
import importlib.machinery
import os
import sys

# torch >= 2.6 loads checkpoints with weights_only=True by default, which rejects the pickled extras (numpy scalars,
# config objects) in many Kaggle checkpoints. The notebooks were written for the old default.
os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")


# Old libraries that notebooks attach as inputs (e.g. timm 0.3) import torch._six, which torch 2 removed. This
# provides the names they used, and only when something imports torch._six; a real torch._six would be found first.
class _TorchSixShim(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path=None, target=None):
        return importlib.machinery.ModuleSpec(name, self) if name == "torch._six" else None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        import collections.abc
        import math
        module.container_abcs = collections.abc
        module.string_classes = (str, bytes)
        module.int_classes = int
        module.inf = math.inf
        module.nan = math.nan


sys.meta_path.append(_TorchSixShim())


# albumentations 1.4 removed transforms that old notebooks still import (often only import, for unused training
# augmentations). Missing names resolve through a module __getattr__: the two brightness/contrast transforms map to
# RandomBrightnessContrast with the other limit at 0 (what they did); imgaug wrappers and Cutout raise if used.
def _albumentations_legacy(module, name):
    if name == "RandomBrightness":
        return lambda limit=0.2, always_apply=False, p=0.5: module.RandomBrightnessContrast(
            brightness_limit=limit, contrast_limit=0, p=p)
    if name == "RandomContrast":
        return lambda limit=0.2, always_apply=False, p=0.5: module.RandomBrightnessContrast(
            brightness_limit=0, contrast_limit=limit, p=p)
    if name.startswith("IAA") or name in ("Cutout", "JpegCompression"):
        def removed(*args, **kwargs):
            raise NotImplementedError(f"albumentations.{name} no longer exists (compat stub, import only)")
        return removed
    raise AttributeError(f"module 'albumentations' has no attribute {name!r}")


class _AlbumentationsLegacyNames(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name != "albumentations":
            return None
        spec = importlib.machinery.PathFinder.find_spec(name, path)
        if spec is None or spec.loader is None:
            return None
        exec_module = spec.loader.exec_module

        def exec_with_legacy(module):
            exec_module(module)
            module.__getattr__ = lambda attr: _albumentations_legacy(module, attr)

        spec.loader.exec_module = exec_with_legacy
        return spec


sys.meta_path.insert(0, _AlbumentationsLegacyNames())
