import os
import impl.rpgmv
from functools import wraps

backend_list = [impl.rpgmv]


def call_backend_by_path(path, backend, action_name, *args, **kwargs):
    suffix = "file" if os.path.isfile(path) else "dir" if os.path.isdir(path) else None

    if suffix is None:
        raise ValueError(f"Invalid path: {path}")

    method = getattr(backend, f"{action_name}_{suffix}", None)
    if not callable(method):
        raise ValueError(f"{backend} does not support {action_name}_{suffix}")

    return method(path, *args, **kwargs)


def guess_game_engine(path):
    for backend in backend_list:
        if call_backend_by_path(path, backend, "can_handle"):
            return backend
    return None


def backend_action(func):
    action_name = func.__name__

    @wraps(func)
    def wrapper(path, *args, **kwargs):
        if backend := guess_game_engine(path):
            return call_backend_by_path(path, backend, action_name, *args, **kwargs)
        else:
            raise ValueError(f"Failed to determine backend: {path}")

    return wrapper


@backend_action
def extract(path):
    pass


@backend_action
def replace(path):
    pass
