import enum

import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import AHTokenBoxArgs


class Face(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


@util.register_svg_variants(Face)
class write_svg(util.VariantSVGFile[AHTokenBoxArgs, Face]):
  def __call__(self, args: AHTokenBoxArgs):
    face = self.variant

    length = ((args.dimension.length + args.thickness) * args.columns) - args.thickness
    height = args.dimension.height

    horizontal = util.Tab(args.tab, args.thickness, args.kerf).h_tabs(True, length, True)
    vertical = util.Tab(args.tab / 2, args.thickness, args.kerf).v_tabs(False, (height / 2) - args.thickness, False)
    top_path = path.d([
        util.h_center(lambda _: util.h_tab(
            out=False,
            thickness=args.magnet.height,
            tab=args.magnet.width,
            kerf=args.kerf,
        ), length + (args.thickness * 2)),
    ])
    right_path = path.d([
        path.d.v(args.thickness),
        vertical,
    ])
    bottom_path = -horizontal
    left_path = -path.d([
        vertical,
        path.d.v(args.thickness),
    ])

    d = path.d([
        path.d.m(0, 0 if face is Face.BOTTOM else args.thickness),
        top_path,
        right_path,
        bottom_path,
        left_path,
    ])

    children: list[Element | str] = [
        path(attrs=path.attrs(
            d=d,
        ) | args.cut),
    ]

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / util.filename(__file__, face), s
