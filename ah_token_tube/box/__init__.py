from .. import shared
from .args import AHTokenBox
from .components import (
    box_end,
    box_face,
    box_h_divider,
    box_side,
    box_v_divider,
)


def runner(args: AHTokenBox):
  return shared.write_svgs(shared.generate_svgs(args))
