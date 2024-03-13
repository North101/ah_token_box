import enum
import pathlib

import pysvg
from pysvg import Element, path, svg

from ...helper import *
from ...shared import *
from ..args import AHTokenBox


class Side(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


class write_svg(RegisterSVGCallable[AHTokenBox]):
  def __init__(self, side: Side):
    self.side = side

  def __call__(self, args: AHTokenBox):
    side = self.side
    helper = Tab(args.tab, args.thickness, args.kerf)

    height = args.dimension.height
    width = ((args.dimension.width + helper.thickness) * args.rows) - helper.thickness

    horizontal = path.d([
        helper.h_side(True, (height / 2) - args.thickness, False),
    ])
    vertical = helper.v_side(True, width, False)
    top_path = path.d([
        path.d.h(args.thickness),
        horizontal,
    ])
    right_path = vertical
    bottom_path = -path.d([
        horizontal,
        path.d.h(args.thickness),
    ])
    left_path = -v_side(
        out=False,
        width=args.thickness,
        height=args.dimension.width,
        gap=args.thickness,
        max_height=width,
        padding=0,
        kerf=args.kerf,
    ) if side is Side.BOTTOM else -path.d.v(vertical.fill_placeholders.height)

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

    stem = pathlib.Path(__file__).stem
    filename = pathlib.Path(f'{stem}_{side.name.lower()}').with_suffix('.svg').name
    return args.output / filename, s


for side in Side:
  register_svg(write_svg(side=side))
