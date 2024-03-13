import math
from typing import Callable

from pysvg import PresentationAttributes, g, path, transforms
from pysvg.attributes.presentation import DrawSegment

from .types import Image


def corner_radius_br(r: float, bite=False):
  return path.d.a(r, r, 0, False, not bite, r, r)


def corner_radius_tl(r: float, bite=False):
  return path.d.a(r, r, 0, False, not bite, r, -r)


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


def seperated(item: DrawSegment, seperator: DrawSegment, count: int):
  if count == 0:
    raise ValueError()
  for _ in range(count - 1):
    yield item
    yield seperator
  yield item


def m_center(segment: Callable[[float, float], DrawSegment], width: float = 0, height: float = 0):
  return path.d([
      path.placeholder(lambda w, h: path.d.m((width - w) / 2, (height - h) / 2)),
      segment(width, height),
      path.placeholder(lambda w, h: path.d.m((width - w) / 2, (height - h) / 2)),
  ])


def tab_kerf(out: bool, kerf: float):
  return -kerf if out else kerf


def h_tab(out: bool, height: float, width: float, kerf: float):
  height = -height if out else height
  return path.d([
      path.d.v(height),
      path.d.h(width - tab_kerf(out, kerf * 2)),
      -path.d.v(height),
  ])


def h_tabs(out: bool, height: float, width: float, gap: float, max_width: float, kerf: float):
  tab = h_tab(out, height, width, kerf)
  seperator = path.d.h(gap + tab_kerf(out, kerf * 2))
  count = math.floor((max_width - tab.width) / (tab.width + seperator.value))
  return path.d(list(seperated(
      item=tab,
      seperator=seperator,
      count=count + 1,
  )))


def h_side(out: bool, height: float, width: float, gap: float, max_width: float, padding: float, kerf: float):
  max_width = max_width + (padding * 2)
  return path.d([
      path.d.h(padding),
      path.d.h(width + tab_kerf(out, kerf)),
      path.placeholder(lambda w, h: h_center(
          segment=lambda max_width: h_tabs(out, height, width, gap, max_width, kerf),
          width=max_width - w,
      )),
      path.d.h(width + tab_kerf(out, kerf)),
      path.d.h(padding),
  ])


def h_center(segment: Callable[[float], DrawSegment], width: float):
  return path.d([
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
      segment(width),
      path.placeholder(lambda w, h: path.d.h((width - w) / 2)),
  ])


def hm_center(segment: Callable[[float], DrawSegment], width: float):
  return m_center(
      segment=lambda w, h: segment(w),
      width=width,
  )


def h_slot(height: float, width: float, kerf: float):
  kerf = kerf * 2
  return path.d([
      path.d.h(width),
      path.d.v(height - kerf),
      -path.d.h(width),
      -path.d.v(height - kerf),
      path.d.m(height - kerf, 0),
  ])


def h_slots(height: float, width: float, gap: float, max_width: float, kerf: float):
  tab = h_slot(height, width, kerf)
  seperator = path.d.m(gap + kerf * 2, 0)
  count = math.floor((max_width - tab.width) / (tab.width + seperator.x))
  return path.d(list(seperated(
      item=tab,
      seperator=seperator,
      count=count + 1,
  )))


def v_tab(out: bool, width: float, height: float, kerf: float):
  width = -width if out else width
  return path.d([
      -path.d.h(width),
      path.d.v(height - tab_kerf(out, kerf * 2)),
      path.d.h(width),
  ])


def v_tabs(out: bool, width: float, height: float, gap: float, max_height: float, kerf: float):
  tab = v_tab(out, width, height, kerf)
  seperator = path.d.v(gap + tab_kerf(out, kerf * 2))
  count = math.floor((max_height - tab.height) / (tab.height + seperator.value))
  return path.d(list(seperated(
      item=tab,
      seperator=seperator,
      count=count + 1,
  )))


def v_side(out: bool, width: float, height: float, gap: float, max_height: float, padding: float, kerf: float):
  max_height = max_height + (padding * 2)
  return path.d([
      path.d.v(padding),
      path.d.v(height + tab_kerf(out, kerf)),
      path.placeholder(lambda w, h: v_center(
          segment=lambda max_height: v_tabs(out, width, height, gap, max_height, kerf),
          height=max_height - h,
      )),
      path.d.v(height + tab_kerf(out, kerf)),
      path.d.v(padding),
  ])


def v_slot(width: float, height: float, kerf: float):
  kerf = kerf * 2
  return path.d([
      path.d.v(height),
      path.d.h(width - kerf),
      -path.d.v(height),
      -path.d.h(width - kerf),
      path.d.m(0, width - kerf),
  ])


def v_slots(width: float, height: float, gap: float, max_height: float, kerf: float):
  tab = v_slot(width, height, kerf)
  seperator = path.d.m(0, gap + kerf * 2)
  count = math.floor((max_height - tab.height) / (tab.height + seperator.y))
  return path.d(list(seperated(
      item=tab,
      seperator=seperator,
      count=count + 1,
  )))


def v_center(segment: Callable[[float], DrawSegment], height: float):
  return path.d([
      path.placeholder(lambda w, h: path.d.v((height - h) / 2)),
      segment(height),
      path.placeholder(lambda w, h: path.d.v((height - h) / 2)),
  ])


def vm_center(segment: Callable[[float], DrawSegment], height: float):
  return m_center(
      lambda w, h: segment(h),
      height=height
  )


class Tab():
  tab: float
  thickness: float
  kerf: float

  def __init__(self, tab: float, thickness: float, kerf: float):
    self.tab = tab
    self.thickness = thickness
    self.kerf = kerf

  def h_tab(self, out: bool):
    return h_tab(
        out=out,
        height=self.thickness,
        width=self.tab,
        kerf=self.kerf,
    )

  def h_tabs(self, out: bool, width: float, gap: float | None = None):
    return h_tabs(
        out=out,
        height=self.thickness,
        width=self.tab,
        gap=gap if gap is not None else self.tab,
        max_width=width,
        kerf=self.kerf,
    )

  def h_side(self, out: bool, width: float, pad: bool, gap: float | None = None):
    return h_side(
        out=out,
        height=self.thickness,
        width=self.tab,
        gap=gap if gap is not None else self.tab,
        max_width=width,
        padding=self.thickness if pad else 0,
        kerf=self.kerf,
    )

  def h_slot(self):
    return h_slot(
        height=self.thickness,
        width=self.tab,
        kerf=self.kerf,
    )

  def h_slots(self, width: float, gap: float | None = None):
    return h_slots(
        height=self.thickness,
        width=self.tab,
        gap=gap if gap is not None else self.tab,
        max_width=width,
        kerf=self.kerf,
    )

  def v_tab(self, out: bool):
    return v_tab(
        out=out,
        width=self.thickness,
        height=self.tab,
        kerf=self.kerf,
    )

  def v_tabs(self, out: bool, height: float, gap: float | None = None):
    return v_tabs(
        out=out,
        width=self.thickness,
        height=self.tab,
        gap=gap if gap is not None else self.tab,
        max_height=height,
        kerf=self.kerf,
    )

  def v_side(self, out: bool, max_height: float, pad: bool, gap: float | None = None):
    return v_side(
        out=out,
        width=self.thickness,
        height=self.tab,
        gap=gap if gap is not None else self.tab,
        max_height=max_height,
        padding=self.thickness if pad else 0,
        kerf=self.kerf,
    )

  def v_slot(self):
    return v_slot(
        width=self.thickness,
        height=self.tab,
        kerf=self.kerf,
    )

  def v_slots(self, height: float, gap: float | None = None):
    return v_slots(
        width=self.thickness,
        height=self.tab,
        gap=gap if gap is not None else self.tab,
        max_height=height,
        kerf=self.kerf,
    )