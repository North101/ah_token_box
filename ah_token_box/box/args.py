import typed_argparse as tap
from pysvg_util import args, types


class AHTokenBoxArgs(args.SVGArgs):
  dimension: types.Dimension = tap.arg(
      help='card dimensions [length] [width] [height] (mm)',
  )
  thickness: float = tap.arg(
      type=types.PositiveFloat,
      help='material thickness (mm)',
  )
  kerf: float = tap.arg(
      type=types.PositiveFloat,
      help='kerf (mm)',
  )
  tab: float = tap.arg(
      type=types.PositiveFloat,
      default=4.0,
      help='tab size (mm)',
  )
  rows: int = tap.arg(
      help='rows',
  )
  columns: int = tap.arg(
      help='columns',
  )
  magnet: types.Size = tap.arg()

  top_image: list[types.Image] | None = tap.arg(
      default=None,
  )
