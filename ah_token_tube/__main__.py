import typed_argparse as tap

from . import box
from .shared import *

if __name__ == '__main__':
  tap.Parser(
      box.AHTokenBox,
  ).bind(
      box.runner,
  ).run()
