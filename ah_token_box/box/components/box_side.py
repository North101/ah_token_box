import enum

import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import AHTokenBoxArgs


class Side(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


@util.register_svg_variants(Side)
class write_svg(util.VariantSVGFile[AHTokenBoxArgs, Side]):
  def __init__(self, side: Side):
    self.side = side

  def __call__(self, args: AHTokenBoxArgs):
    side = self.side
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    height = args.dimension.height
    width = args.dimension.width * args.rows

    horizontal = path.d([
        helper.h_tabs(True, (height / 2) - args.thickness, False),
    ])
    vertical = helper.v_tabs(True, width, False)
    top_path = path.d([
        path.d.h(args.thickness),
        horizontal,
    ])
    right_path = vertical
    bottom_path = -path.d([
        horizontal,
        path.d.h(args.thickness),
    ])
    left_path = -path.d.v(vertical.fill_placeholders.height)

    d = path.d([
        path.d.m(0, helper.thickness),
        top_path,
        right_path,
        bottom_path,
        left_path,
    ])

    children: list[Element | str] = [
        path(attrs=path.attrs(
            d=d,
        ) | args.cut | path.attrs(fill='red')),
    ]

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / util.filename(__file__, side), s
