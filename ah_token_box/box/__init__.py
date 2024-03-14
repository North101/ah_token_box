import pysvg_util as util

from .args import AHTokenBoxArgs
from .components import *


def runner(args: AHTokenBoxArgs):
  return util.write_svgs(util.generate_svgs(args))
