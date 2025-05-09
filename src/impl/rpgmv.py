import os
import json
from pathlib import Path


def extract_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        print(path)


def extract_dir(path):
    for file in select_files(path):
        extract_file(file)


def can_handle_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            head = json.load(f)

            return all(
                "code" in code and "parameters" in code
                for event in head["events"][1:]
                for page in event["pages"]
                for code in page["list"]
            )

    except Exception:
        return False


def can_handle_dir(path):
    return "package.json" in os.listdir(path)


def select_files(dir):
    data_dir = Path(dir) / "data"

    return [path for path in data_dir.glob("*.json") if can_handle_file(path)]
