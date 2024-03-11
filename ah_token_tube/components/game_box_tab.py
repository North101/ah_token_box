import pathlib

import pysvg
from pysvg import Element, path, svg

from ..args import AHTokenTube
from ..helper import Helper
from ..shared import *


@register_svg
class write_svg(RegisterSVGCallable[AHTokenTube]):
  def __call__(self, args: AHTokenTube):
    helper = Helper(args.tab, args.thickness, args.kerf)
    length = args.dimension.length / 2

    top_path = path.d.h(length)
    right_path = path.d.v(args.thickness)
    bottom_path = -path.d([
        path.placeholder(lambda w, h: path.d.h((length - w) / 2)),
        helper.h_tab(True, False),
        path.placeholder(lambda w, h: path.d.h((length - w) / 2)),
    ])
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
