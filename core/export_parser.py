import json
from pathlib import Path


class ExportParser:

    def __init__(self, json_path):
        self.json_path = Path(json_path)

    def load(self):

        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)