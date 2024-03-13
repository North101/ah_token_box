import enum
import pathlib

import pysvg
from pysvg import Element, path, svg

from ...util import *
from ..args import AHTokenBoxArgs


class End(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


@register_svgs(End)
class write_svg(RegisterSVGCallable[AHTokenBoxArgs]):
  def __init__(self, end: End):
    self.end = end

  def __call__(self, args: AHTokenBoxArgs):
    end = self.end
    helper = Tab(args.tab, args.thickness, args.kerf)

    length = ((args.dimension.length + helper.thickness) * args.columns) - helper.thickness
    width = ((args.dimension.width + helper.thickness) * args.rows) - helper.thickness

    horizontal = helper.h_tabs(False, length, True)
    vertical = helper.v_tabs(False, width, True)
    top_path = horizontal
    right_path = vertical
    bottom_path = -horizontal
    left_path = -vertical

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
        ) | args.cut | path.attrs(fill='red')),
    ]

    slots = path.d(list(seperated(
        item=path.d([
            path.d.v(args.thickness + -args.kerf + -args.kerf),
            -path.d.h(args.thickness),
            -path.d.v(args.thickness + -args.kerf + -args.kerf),
            path.d.h(args.thickness),
            path.d.m(0, args.thickness + -args.kerf + -args.kerf),
        ]),
        seperator=path.d.m(0, args.dimension.width),
        count=args.rows - 1,
    )))
    if end is End.BOTTOM:
      children += [
          g(
              attrs=g.attrs(
                  transform=transforms.translate(x=args.thickness, y=args.thickness),
              ),
              children=[
                  path(attrs=path.attrs(
                      transform=transforms.translate(x=i * (args.dimension.length + helper.thickness)),
                      d=vm_center(lambda length: slots, height=width),
                  ))
                  for i in range(1, args.columns)
              ],
          )
      ]

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / filename(__file__, end), s
