import typed_argparse as tap

from . import box
from .shared import *


def main():
  tap.Parser(
      box.AHTokenBox,
  ).bind(
      box.runner,
  ).run()
