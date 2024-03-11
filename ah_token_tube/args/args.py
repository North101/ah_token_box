import typed_argparse as tap

from ah_token_tube import types
from ah_token_tube.shared import *

from . import const


class AHTokenTube(SVGArgs):
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
      default=const.TAB,
      help='tab size (mm)',
  )
  count: int = tap.arg(
      help='tab size (mm)',
  )

  face_image: Image | None = tap.arg(
      default=None,
  )
  front_image: Image | None = tap.arg(
      default=None,
  )
  back_image: Image | None = tap.arg(
      default=None,
  )
