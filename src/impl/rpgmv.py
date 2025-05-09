import os
import json
from pathlib import Path
import enum


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
    result = []
    for opcode in lis:
        if r := extract_opcode(opcode):
            if isinstance(r, list):
                result += r
            else:
                result.append(r)
    return result


def for_each_list(head, func):
    return [
        item
        for event in head["events"][1:]
        for page in event["pages"]
        for item in func(page["list"])
    ]


def extract_file(path):
    with open(path, "r", encoding="utf-8") as f:
        head = json.load(f)
        return for_each_list(head, extract_list)


def select_files(dir):
    data_dir = Path(dir) / "data"
    return [path for path in data_dir.glob("*.json") if can_handle_file(path)]


def extract_dir(path):
    result = []
    for file in select_files(path):
        result += extract_file(file)

    return result


def can_handle_file(path):
    try:
        extract_file(path)
        return True
    except Exception:
        return False


def can_handle_dir(path):
    return "package.json" in os.listdir(path)
