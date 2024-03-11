from .. import shared
from .args import AHTokenTube
from .components import (
    game_box_end,
    game_box_face,
    game_box_side,
    game_box_tab,
)


def runner(args: AHTokenTube):
  return shared.write_svgs(shared.generate_svgs(args))
