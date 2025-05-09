import os
import json
import enum
import itertools


@enum.unique
class Code(enum.IntEnum):
    ShowChoicess = 102
    ShowText = 401


def get_first_param(param):
    return param[0]


extractor_table = {
    Code.ShowText: get_first_param,
    Code.ShowChoicess: get_first_param,
}


def extract_opcode(opcode):
    code = opcode["code"]
    param = opcode["parameters"]

    if code in Code and (extract := extractor_table.get(code)):
        return extract(param)


def extract_list(lis):
    for opcode in lis:
        if r := extract_opcode(opcode):
            if isinstance(r, list):
                yield from r
            else:
                yield r


def for_each_list(head, func):
    for event in head["events"][1:]:
        for page in event["pages"]:
            yield func(page["list"])


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_file(path):
    data = read_file(path)
    return itertools.chain.from_iterable(for_each_list(data, extract_list))


def select_files(dir):
    data_dir = os.path.join(dir, "data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            path = os.path.join(data_dir, filename)
            if can_handle_file(path):
                yield path


def extract_dir(path):
    for file in select_files(path):
        yield from extract_file(file)


def can_handle_file(path):
    try:
        for item in extract_file(path):
            pass
        return True
    except Exception:
        return False


def can_handle_dir(path):
    return "package.json" in os.listdir(path)
