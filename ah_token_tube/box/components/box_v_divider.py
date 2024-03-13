import pathlib

import pysvg
from pysvg import Element, path, svg
from pysvg.attributes.presentation import DrawSegment

from ...helper import *
from ...shared import *
from ..args import AHTokenBox


@register_svg
class write_svg(RegisterSVGCallable[AHTokenBox]):
  def __call__(self, args: AHTokenBox):
    height = args.dimension.height / 2

    top_path = path.d(list(seperated(
        item=path.d.h(args.dimension.width),
        seperator=path.d([
            path.d.v(height / 2),
            path.d.h(args.thickness),
            -path.d.v(height / 2),
        ]),
        count=args.rows,
    )))
    right_path = path.d.v(height)
    bottom_path = -h_center(
        lambda _: path.d(list(seperated(
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
        h_length=top_path.fill_placeholders.width,
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

    filename = pathlib.Path(__file__).with_suffix('.svg').name
    return args.output / filename, s
