import os
import impl.rpgmv

backend = [impl.rpgmv]


def guess_game_engine(path):
    for item in backend:
        if os.path.isfile(path) and item.can_handle_file(path):
            return item

        elif os.path.isdir(path) and item.can_handle_dir(path):
            return item

        else:
            return False


def extract(path, ftype=None):
    if backend := guess_game_engine(path):
        if os.path.isfile(path):
            return backend.extract_file(path)

        elif os.path.isdir(path):
            return backend.extract_dir(path)
