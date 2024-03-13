import typed_argparse as tap

from .. import shared, types


class AHTokenBox(shared.SVGArgs):
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
      help='tab size (mm)',
  )
  columns: int = tap.arg(
      help='tab size (mm)',
  )
  magnet: types.Size = tap.arg()

  face_image: types.Image | None = tap.arg(
      default=None,
  )
  front_image: types.Image | None = tap.arg(
      default=None,
  )
  back_image: types.Image | None = tap.arg(
      default=None,
  )
