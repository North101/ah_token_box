import pysvg
import pysvg_util as util
from pysvg import Element, path, svg
from pysvg.attributes.presentation import DrawSegment

from ..args import AHTokenBoxArgs


@util.register_svg()
class write_svg(util.RegisterSVGCallable[AHTokenBoxArgs]):
  def __call__(self, args: AHTokenBoxArgs):
    height = args.dimension.height / 2

    top_path = path.d([
        -path.d.v(args.thickness),
        path.d.h(args.thickness),
        path.d.v(args.thickness),
        path.placeholder(lambda w, h: path.d.h(
            ((args.dimension.length + args.thickness) * args.columns) - args.thickness - args.thickness - h)),
        -path.d.v(args.thickness),
        path.d.h(args.thickness),
        path.d.v(args.thickness),
    ])
    right_path = path.d([
        path.d.h(args.thickness),
        path.d.v(height / 2),
        -path.d.h(args.thickness),
        path.d.v(height / 2),
    ])
    bottom_path = -path.d(list(util.seperated(
        item=path.d.h(args.dimension.length),
        seperator=path.d([
            path.d.v(height / 2),
            path.d.h(args.thickness),
            -path.d.v(height / 2),
        ]),
        count=args.columns,
    )))
    left_path = -path.d([
        path.d.v(height / 2),
        path.d.h(args.thickness),
        path.d.v(height / 2),
        -path.d.h(args.thickness),
    ])

    d = path.d([
        path.d.m(args.thickness, args.thickness),
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
