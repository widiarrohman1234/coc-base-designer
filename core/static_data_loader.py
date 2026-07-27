from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional


class StaticDataLoader:
    """
    Load Clash of Clans static_data.json.

    Features
    --------
    - Load JSON once
    - Build O(1) lookup tables
    - Search by ID
    - Search by name
    """

    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)

        with open(self.json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.buildings: List[dict] = self.data.get("buildings", [])

        # Fast lookup
        self._id_map: Dict[int, dict] = {
            item["_id"]: item
            for item in self.buildings
        }

        self._name_map: Dict[str, dict] = {
            item["name"].lower(): item
            for item in self.buildings
        }

    # --------------------------------------------------
    # Basic getters
    # --------------------------------------------------

    def get_building(self, building_id) -> Optional[dict]:
        try:
            building_id = int(building_id)
        except (TypeError, ValueError):
            return None

        return self._id_map.get(building_id)

    def get_building_name(self, building_id: int) -> Optional[str]:
        obj = self.get_building(building_id)
        return None if obj is None else obj["name"]

    def get_building_by_name(self, name: str) -> Optional[dict]:
        return self._name_map.get(name.lower())

    def exists(self, building_id: int) -> bool:
        return building_id in self._id_map

    def all_buildings(self) -> List[dict]:
        return self.buildings

    def total_buildings(self) -> int:
        return len(self.buildings)

    def total_buildings(self):
        return len(self.buildings)

# How to use
# from static_data_loader import StaticDataLoader
# loader = StaticDataLoader("data/static_data.json")
# print(loader.get_building_name(1000001)) # Town Hall
# Mendapatkan seluruh informasi
# print(loader.get_building(1000001))
# Pencarian berdasarkan nama
# print(loader.get_building_by_name("Wizard Tower"))

# print(loader.total_buildings())
# print(len(loader._id_map))
# print(list(loader._id_map.keys())[:10])
# print(type(next(iter(loader._id_map.keys()))))
# print(1000001 in loader._id_map)
# print(loader._id_map.get(1000001))
