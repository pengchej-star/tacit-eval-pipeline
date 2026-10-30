# Installed as sitecustomize.py in the kaggle-run-gpu venv's site-packages.
# Old libraries that notebooks attach as inputs (e.g. timm 0.3) import torch._six, which torch 2 removed. This
# provides the names they used, and only when something imports torch._six; a real torch._six would be found first.
import importlib.abc
import importlib.machinery
import sys


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
