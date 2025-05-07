import os
import json
from pathlib import Path

class RPGMV:
    def extract_file(self, path):
        with open(path, 'r', encoding="utf-8") as f:
            content = f.read()
            print(path)
        
    def extract_dir(self, path):
        for file in self.select_files(path):
            self.extract_file(file)

    def can_handle_file(self, path):
        try:
            with open(path, 'r', encoding="utf-8") as f:
                head = json.load(f)

                return all(
                    "code" in code and "parameters" in code
                    
                    for event in head["events"][1:]
                    for page in event["pages"]
                    for code in page["list"]
                )

        except Exception:
            return False

    def can_handle_dir(self, path):
        return "package.json" in os.listdir(path)

    def select_files(self, dir):
        return [path for path in Path(dir).glob("*.json") if self.can_handle_file(path)]