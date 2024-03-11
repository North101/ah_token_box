import pathlib
from typing import Any, Type

import typed_argparse as tap
from pysvg import PresentationAttributes, g, path, svg, transforms

from .types import Image


class SVGArgs(tap.TypedArgs):
  output: pathlib.Path = tap.arg(
      default=pathlib.Path('output'),
      help='output path',
  )

  cut = PresentationAttributes(
      fill='none',
      stroke='black',
      stroke_width=0.001,
  )

  engrave = PresentationAttributes(
      fill='black',
      stroke='none',
      stroke_width=0.001,
  )


class RegisterSVGCallable[T: SVGArgs]():
  def __call__(self, args: T) -> tuple[pathlib.Path, svg]:
    ...


svg_list: list[RegisterSVGCallable[Any]] = []


def register_svg[T: SVGArgs](f: RegisterSVGCallable[T] | Type[RegisterSVGCallable[T]]):
  svg_list.append(f() if isinstance(f, Type) else f)
  return f


def generate_svgs(args: SVGArgs):
  args.output.mkdir(parents=True, exist_ok=True)
  data = [
      write_svg(args)
      for write_svg in svg_list
      if isinstance(args, write_svg.__call__.__annotations__.get('args', tuple()))
  ]
  for (filename, svg_data) in data:
    filename.write_text(format(svg_data, '.3f'))

  return data


def write_svgs(svgs: list[tuple[pathlib.Path, svg]]):
  data = [
      (str(filename), svg.attrs.width, svg.attrs.height)
      for (filename, svg) in svgs
  ]
  name_len = max(len(name) for (name, _, _) in data)
  length_len = max(len(f'{length:.2f}') for (_, length, _) in data)
  height_len = max(len(f'{height:.2f}') for (_, _, height) in data)
  for (name, length, height) in data:
    print(f'{name:<{name_len}} @ {length:>{length_len}.3f} x {height:>{height_len}.3f}')
