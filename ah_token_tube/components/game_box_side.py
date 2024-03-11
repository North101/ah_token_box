import enum
import pathlib

import pysvg
from pysvg import Element, path, svg

from ..args import AHTokenTube
from ..helper import Helper
from ..shared import *


class Side(enum.Enum):
  RIGHT = enum.auto()
  LEFT = enum.auto()


class write_svg(RegisterSVGCallable[AHTokenTube]):
  def __init__(self, side: Side):
    self.side = side

  def __call__(self, args: AHTokenTube):
    side = self.side
    helper = Helper(args.tab, args.thickness, args.kerf)

    width = ((args.dimension.width + helper.thickness) * args.count) - helper.thickness
    height = args.dimension.height

    horizontal = helper.h_side(True, width, False)
    vertical = helper.v_side(True, height, False)
    if side is side.LEFT:
      top_path = path.d.h(horizontal.fill_placeholders.width)
      right_path = helper.v_center(
          lambda _: path.d([
              -path.d.h(3),
              path.d.v(3),
              path.d.h(3),
          ]),
          v_length=vertical.fill_placeholders.height,
      )
      bottom_path = -horizontal
      left_path = -vertical
    else:
      top_path = horizontal
      right_path = vertical
      bottom_path = -path.d.h(horizontal.fill_placeholders.width)
      left_path = -helper.v_center(
          lambda _: path.d([
              -path.d.h(3),
              path.d.v(3),
              path.d.h(3),
          ]),
          v_length=vertical.fill_placeholders.height,
      )

    d = path.d([
        path.d.m(helper.thickness if side is side.LEFT else 0, 0 if side is side.LEFT else helper.thickness),
        top_path,
        right_path,
        bottom_path,
        left_path,
    ])

    slot = helper.v_slot()
    slot_x = helper.thickness if side is Side.LEFT else 0
    slot_y = (vertical.fill_placeholders.height - slot.fill_placeholders.height) / 2

    children: list[Element | str] = [
        path(attrs=path.attrs(
            d=d,
        ) | args.cut | path.attrs(fill='red')),
        g(
            attrs=g.attrs(
                transform=transforms.translate(x=slot_x, y=slot_y)
            ),
            children=[
                path(attrs=path.attrs(
                    transform=transforms.translate(
                        x=(i * (args.dimension.width + helper.thickness)),
                        y=0,
                    ),
                    d=slot,
                ) | args.cut | path.attrs(fill='blue'))
                for i in range(1, args.count)
            ],
        ),
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
