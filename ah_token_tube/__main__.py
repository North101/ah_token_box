import typed_argparse as tap

from . import AHTokenTube, runner
from .shared import *

if __name__ == '__main__':
  tap.Parser(
      AHTokenTube,
  ).bind(
      runner,
  ).run()
