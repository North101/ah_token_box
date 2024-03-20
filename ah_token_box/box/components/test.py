import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import AHTokenBoxArgs


@util.register_svg()
class write_svg(util.SVGFile[AHTokenBoxArgs]):
  def __call__(self, args: AHTokenBoxArgs):
    d = path.d([
        path.d.m(0, 0),
        util.h_center(
            segment=lambda _: util.h_tab(
                out=False,
                thickness=args.thickness,
                tab=args.thickness,
                kerf=args.kerf
            ),
            width=10,
        ),
        util.v_center(
            segment=lambda _: util.v_tab(
                out=False,
                thickness=args.thickness,
                tab=args.thickness,
                kerf=args.kerf,
            ),
            height=15,
        ),
        -path.d.h(10),
        -path.d.v(15),
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

    return util.filename(__file__), s
