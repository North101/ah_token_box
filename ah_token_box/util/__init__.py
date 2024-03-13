import importlib
import pkgutil

from .args import *
from .output import *
from .svg import *


def import_submodules(path, name):
  for loader, module_name, is_pkg in pkgutil.walk_packages(path, f'{name}.'):
    importlib.import_module(module_name, '*')
