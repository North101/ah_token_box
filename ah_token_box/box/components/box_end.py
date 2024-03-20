import enum

import pysvg
import pysvg_util as util
from pysvg import Element, g, path, svg, transforms

from ..args import AHTokenBoxArgs


class End(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


@util.register_svg_variants(End)
class write_svg(util.VariantSVGFile[AHTokenBoxArgs, End]):
  def __call__(self, args: AHTokenBoxArgs):
    end = self.variant
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = ((args.dimension.length + helper.thickness) * args.columns) - helper.thickness
    width = args.dimension.width * args.rows

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
        ) | args.cut),
    ]

    slots = util.v_slots(
        thickness=args.thickness,
        slot=args.tab,
        gap=args.dimension.width,
        max_height=width,
        padding=args.thickness,
        kerf=args.kerf,
    )
    if end is End.BOTTOM:
      children += [
          g(
              attrs=g.attrs(
                  transform=transforms.translate(0, y=args.thickness),
              ),
              children=[
                  path(attrs=path.attrs(
                      transform=transforms.translate(x=i * (args.dimension.length + helper.thickness)),
                      d=util.vm_center(lambda length: slots, height=width),
                  ) | args.cut)
                  for i in range(1, args.columns)
              ],
          )
      ]

    if self.variant is End.TOP and args.top_image:
      if len(args.top_image) == 1:
        children.append(util.engrave_image(
            parent=d,
            image=args.top_image[0],
            engrave=args.engrave,
        ))
      elif len(args.top_image) == args.columns:
        children += [
            g(attrs=g.attrs(
                transform=transforms.translate(
                    x=(args.dimension.length + args.thickness) * i,
                    y=0,
                ),
            ), children=[
                util.engrave_image(
                    parent=(args.dimension.length, d.height),
                    image=args.top_image[i],
                    engrave=args.engrave,
                ),
            ])
            for i in range(args.columns)
        ]
      else:
        raise ValueError()

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return util.filename(__file__, end), s
