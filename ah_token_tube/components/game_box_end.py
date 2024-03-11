import enum
import pathlib

import pysvg
from pysvg import Element, path, svg

from ..args import AHTokenTube
from ..helper import Helper
from ..shared import *


class End(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


class write_svg(RegisterSVGCallable[AHTokenTube]):
  def __init__(self, end: End):
    self.end = end

  def __call__(self, args: AHTokenTube):
    end = self.end
    helper = Helper(args.tab, args.thickness, args.kerf)

    length = args.dimension.length
    width = ((args.dimension.width + helper.thickness) * args.count) - helper.thickness

    horizontal = helper.h_side(True, length, True)
    vertical = helper.v_side(False, width, False)
    if end is End.BOTTOM:
      top_path = helper.h_center(
          lambda _: path.d([
              path.d.v(3),
              path.d.h(3),
              -path.d.v(3),
          ]),
          h_length=horizontal.fill_placeholders.width,
      )
      right_path = path.d.v(vertical.fill_placeholders.height)
      bottom_path = -horizontal
      left_path = -vertical
    else:
      top_path = horizontal
      right_path = vertical
      bottom_path = -helper.h_center(
          lambda _: path.d([
              path.d.v(3),
              path.d.h(3),
              -path.d.v(3),
          ]),
          h_length=horizontal.fill_placeholders.width,
      )
      left_path = -path.d.v(vertical.fill_placeholders.height)

    d = path.d([
        path.d.m(0, helper.thickness if end is End.TOP else 0),
        top_path,
        right_path,
        bottom_path,
        left_path,
    ])

    slot = helper.h_slot()
    slot_x = (horizontal.fill_placeholders.width - slot.fill_placeholders.width) / 2
    slot_y = -helper.thickness if end is End.BOTTOM else 0

    a = [
        'Roland Banks',
        'Daisy Walker',
        '"Skids" O\'Toole',
        'Agnes Baker',
        'Wendy Adams',
    ]

    children: list[Element | str] = [
        path(attrs=path.attrs(
            d=d,
        ) | args.cut | path.attrs(fill='red')),
        g(
            attrs=g.attrs(
                transform=transforms.translate(x=slot_x, y=slot_y),
            ),
            children=[
                path(attrs=path.attrs(
                    transform=transforms.translate(
                        x=0,
                        y=(i * (args.dimension.width + helper.thickness)),
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
    filename = pathlib.Path(f'{stem}_{end.name.lower()}').with_suffix('.svg').name
    return args.output / filename, s


for end in End:
  register_svg(write_svg(end=end))
