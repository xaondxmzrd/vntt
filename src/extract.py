import os
import guess


def extract(path, ftype=None):
    if backend := guess.guess_game_engine(path):
        if os.path.isfile(path):
            backend.extract_file(path)

        elif os.path.isdir(path):
            backend.extract_dir(path)
