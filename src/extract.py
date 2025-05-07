import os
import guess


def extract(path, ftype=None):
    if impl := guess.guess_game_engine(path):
        if os.path.isfile(path):
            impl.extract_file(path)

        elif os.path.isdir(path):
            impl.extract_dir(path)
