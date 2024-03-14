import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import AHTokenBoxArgs


@util.register_svg()
class write_svg(util.RegisterSVGCallable[AHTokenBoxArgs]):
  def __call__(self, args: AHTokenBoxArgs):
    height = args.dimension.height / 2

    top_path = path.d(list(util.seperated(
        item=path.d.h(args.dimension.width),
        seperator=path.d([
            path.d.v(height / 2),
            path.d.h(args.thickness),
            -path.d.v(height / 2),
        ]),
        count=args.rows,
    )))
    right_path = path.d.v(height)
    bottom_path = -util.h_center(
        lambda _: path.d(list(util.seperated(
            item=path.d([
                path.d.h(args.kerf),
                -path.d.v(args.thickness),
                path.d.h(args.thickness - args.kerf - args.kerf),
                path.d.v(args.thickness),
                path.d.h(args.kerf),
            ]),
            seperator=path.d.h(args.dimension.width),
            count=args.rows - 1,
        ))),
        width=top_path.fill_placeholders.width,
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
