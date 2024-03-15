import enum

import pysvg
import pysvg_util as util
from pysvg import Element, path, svg

from ..args import AHTokenBoxArgs


class Face(enum.Enum):
  TOP = enum.auto()
  BOTTOM = enum.auto()


@util.register_svg_variants(Face)
class write_svg(util.VariantSVGFile[AHTokenBoxArgs, Face]):
  def __call__(self, args: AHTokenBoxArgs):
    face = self.variant
    helper = util.Tab(args.tab, args.thickness, args.kerf)

    length = ((args.dimension.length + helper.thickness) * args.columns) - helper.thickness
    height = args.dimension.height

    horizontal = helper.h_tabs(True, length, True)
    vertical = helper.v_tabs(False, (height / 2) - args.thickness, False)
    top_path = path.d([
        path.d.h(args.thickness),
        path.d.v(args.thickness if face is Face.BOTTOM else -args.thickness),
        *util.seperated_by(
            items=[util.h_center(lambda _: util.h_tab(
                out=False,
                thickness=args.magnet.height,
                tab=args.magnet.width,
                kerf=args.kerf,
            ), args.dimension.length)] * args.columns,
            seperator=path.d.h(args.thickness),
        ),
        -path.d.v(args.thickness if face is Face.BOTTOM else -args.thickness),
        path.d.h(args.thickness),
    ])
    right_path = path.d([
        path.d.v(args.thickness * 2 if face is Face.BOTTOM else 0),
        vertical,
    ])
    bottom_path = -horizontal
    left_path = -path.d([
        vertical,
        path.d.v(args.thickness * 2 if face is Face.BOTTOM else 0),
    ])

    d = path.d([
        path.d.m(0, 0 if face is Face.BOTTOM else args.thickness),
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

    image = args.face_image
    if image:
      children.append(util.engrave_image(
          path=d,
          image=image,
          engrave=args.engrave,
      ))

    s = svg(
        attrs=svg.attrs(
            width=pysvg.length(d.width, 'mm'),
            height=pysvg.length(d.height, 'mm'),
            viewBox=(0, 0, d.width, d.height),
        ),
        children=children,
    )

    return args.output / util.filename(__file__, face), s
