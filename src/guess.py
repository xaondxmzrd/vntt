import os
from impl.rpgmv import RPGMV

impl = [RPGMV()]


def guess_game_engine(path):
    for item in impl:
        if os.path.isfile(path) and item.can_handle_file(path):
            return item

        elif os.path.isdir(path) and item.can_handle_dir(path):
            return item

        else:
            return False
