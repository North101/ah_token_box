import math
from typing import Callable

from pysvg import PresentationAttributes, g, path, svg, transforms
from pysvg.attributes.presentation import DrawSegment

from .types import Image


class Helper():
  tab: float
  thickness: float
  kerf: float

  def __init__(self, tab: float, thickness: float, kerf: float):
    self.tab = tab
    self.thickness = thickness
    self.kerf = kerf

  def h_tab_half(self):
    return path.d.h(self.tab / 2)

  def h_tab(self, out: bool, padding: float | None = None):
    padding = padding if padding is not None else self.tab / 2
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.v(self.thickness) if out else path.d.v(self.thickness)
    return path.d([
        path.d.h(padding + kerf),
        thickness,
        path.d.h(self.tab + -kerf + -kerf),
        -thickness,
        path.d.h(kerf + padding),
    ])

  def h_tabs(self, out: bool, width: float, padding: float | None = None):
    h_tab = self.h_tab(out, padding)
    count = math.floor(width / h_tab.width)
    return path.d([
        h_tab
        for _ in range(count)
    ])

  def v_tab_half(self):
    return path.d.v(self.tab / 2)

  def v_tab(self, out: bool, padding: float | None = None):
    padding = padding if padding is not None else self.tab / 2
    kerf = -self.kerf if out else self.kerf
    thickness = -path.d.h(self.thickness) if out else path.d.h(self.thickness)
    return path.d([
        path.d.v(padding + kerf),
        -thickness,
        path.d.v(self.tab + -kerf + -kerf),
        thickness,
        path.d.v(kerf + padding),
    ])

  def v_tabs(self, out: bool, height: float, padding: float | None = None):
    v_tab = self.v_tab(out, padding)
    count = math.floor(height / v_tab.height)
    return path.d([
        v_tab
        for _ in range(count)
    ])

  def h_slot(self):
    kerf = self.kerf
    thickness = path.d.v(self.thickness)
    return path.d([
        path.d.m((self.tab / 2) + kerf, 0),
        thickness,
        path.d.h(self.tab + -kerf + -kerf),
        -thickness,
        -path.d.h(self.tab + -kerf + -kerf),
        path.d.m(self.tab + -kerf + -kerf, 0),
        path.d.m(kerf + (self.tab / 2), 0),
    ])

  def h_slots(self, width: float):
    h_slot = self.h_slot()
    count = math.floor(width / h_slot.width)
    return path.d([
        h_slot
        for _ in range(count)
    ])

  def v_slot(self):
    kerf = self.kerf
    thickness = path.d.h(self.thickness)
    return path.d([
        path.d.m(0, (self.tab / 2) + kerf),
        path.d.v(self.tab + -kerf + -kerf),
        -thickness,
        -path.d.v(self.tab + -kerf + -kerf),
        thickness,
        path.d.m(0, self.tab + -kerf + -kerf),
        path.d.m(0, kerf + (self.tab / 2)),
    ])

  def v_slots(self, height: float):
    v_slot = self.v_slot()
    count = math.floor(height / v_slot.height)
    return path.d([
        v_slot
        for _ in range(count)
    ])

  def h_center(self, segment: Callable[[float], DrawSegment], h_length: float):
    return path.d([
        path.placeholder(lambda w, h: path.d.h((h_length - w) / 2)),
        segment(h_length),
        path.placeholder(lambda w, h: path.d.h((h_length - w) / 2)),
    ])

  def hm_center(self, segment: Callable[[float], DrawSegment], h_length: float):
    return path.d([
        path.placeholder(lambda w, h: path.d.m((h_length - w) / 2, 0)),
        segment(h_length),
        path.placeholder(lambda w, h: path.d.m((h_length - w) / 2, 0)),
    ])

  def v_center(self, segment: Callable[[float], DrawSegment], v_length: float):
    return path.d([
        path.placeholder(lambda w, h: path.d.v((v_length - h) / 2)),
        segment(v_length),
        path.placeholder(lambda w, h: path.d.v((v_length - h) / 2)),
    ])

  def vm_center(self, segment: Callable[[float], DrawSegment], v_length: float):
    return path.d([
        path.placeholder(lambda w, h: path.d.m(0, (v_length - h) / 2)),
        segment(v_length),
        path.placeholder(lambda w, h: path.d.m(0, (v_length - h) / 2)),
    ])

  def h_side(self, out: bool, h_length: float, pad: bool):
    return path.d([
        path.d.h(self.thickness if pad else 0),
        self.h_tab_half(),
        path.placeholder(lambda w, h: self.h_center(
            segment=lambda h_length: self.h_tabs(out, h_length),
            h_length=h_length - w + (self.thickness * 2 if pad else 0),
        )),
        self.h_tab_half(),
        path.d.h(self.thickness if pad else 0),
    ])

  def v_side(self, out: bool, v_length: float, pad: bool):
    return path.d([
        path.d.v(self.thickness if pad else 0),
        self.v_tab_half(),
        path.placeholder(lambda w, h: self.v_center(
            segment=lambda v_length: self.v_tabs(out, v_length),
            v_length=v_length - h + (self.thickness * 2 if pad else 0),
        )),
        self.v_tab_half(),
        path.d.v(self.thickness if pad else 0),
    ])


def engrave_image(path: path.d, image: Image, engrave: PresentationAttributes):
  contain_scale = min(path.width / image.width, path.height / image.height)
  width = image.width * contain_scale * image.scale
  height = image.height * contain_scale * image.scale
  return g(
      attrs=g.attrs(transform=[
          transforms.translate(
              x=(path.width - width) / 2,
              y=(path.height - height) / 2,
          ),
          transforms.scale(contain_scale),
          transforms.scale(image.scale),
      ]) | engrave,
      children=[
          image.path.read_text().strip(),
      ],
  )
