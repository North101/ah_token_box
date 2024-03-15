import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import AHTokenBoxArgs


@util.register_svg()
class write_svg(util.SVGFile[AHTokenBoxArgs]):
  def __call__(self, args: AHTokenBoxArgs):
    height = args.dimension.height / 2
    width = args.dimension.width * args.rows

    top_path = path.d.h(width)
    right_path = path.d.v(height)
    bottom_path = -util.h_tabs(
        out=True,
        thickness=args.thickness,
        tab=args.tab,
        gap=args.dimension.width,
        max_width=width,
        kerf=args.kerf,
    )
    left_path = -right_path

    d = path.d([
        path.d.m(0, 0),
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

    return args.output / util.filename(__file__), s
