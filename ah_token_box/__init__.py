import typed_argparse as tap

from . import box


def main():
  tap.Parser(
      box.AHTokenBoxArgs,
  ).bind(
      box.runner,
  ).run()
