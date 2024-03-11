import enum
import pathlib

import pysvg
from pysvg import Element, circle, path, svg

from ..args import AHTokenTube
from ..helper import Helper, engrave_image
from ..shared import *


class Face(enum.Enum):
  FRONT = enum.auto()
  BACK = enum.auto()


class write_svg(RegisterSVGCallable[AHTokenTube]):
  def __init__(self, face: Face):
    self.face = face

  def __call__(self, args: AHTokenTube):
    face = self.face
    helper = Helper(args.tab, args.thickness, args.kerf)

    length = args.dimension.length
    height = args.dimension.height

    horizontal = helper.h_side(False, length, True)
    vertical = helper.v_side(False, height, True)
    if face is Face.FRONT:
      top_path = path.d.h(horizontal.fill_placeholders.width)
      right_path = path.d.v(vertical.fill_placeholders.height)
      bottom_path = -horizontal
      left_path = -vertical
    else:
      top_path = horizontal
      right_path = vertical
      bottom_path = -path.d.h(horizontal.fill_placeholders.width)
      left_path = -path.d.v(vertical.fill_placeholders.height)

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
        circle(attrs=circle.attrs(
            cx=horizontal.fill_placeholders.width / 2,
            cy=horizontal.fill_placeholders.width - 1.5 if face is not Face.FRONT else 1.51,
            r=1.5,
        ) | args.cut),
        circle(attrs=circle.attrs(
            cx=horizontal.fill_placeholders.width - 1.5 if face is Face.FRONT else 1.51,
            cy=vertical.fill_placeholders.height / 2,
            r=1.5,
        ) | args.cut),
    ]

    if face is Face.FRONT and args.front_image:
      image = args.front_image
    elif face is Face.BACK and args.back_image:
      image = args.back_image
    else:
      image = args.face_image
    if image:
      children.append(engrave_image(
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

    stem = pathlib.Path(__file__).stem
    filename = pathlib.Path(f'{stem}_{face.name.lower()}').with_suffix('.svg').name
    return args.output / filename, s


for face in Face:
  register_svg(write_svg(face=face))
