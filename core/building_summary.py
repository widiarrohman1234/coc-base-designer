from collections import OrderedDict


class BuildingSummary:

    MAP_SIZE = 44

    def __init__(self, export_data, static_loader):
        self.export_data = export_data
        self.static_loader = static_loader

    def summarize(self):

        buildings_summary = OrderedDict()

        townhall_level = None
        building_count = 0
        wall_count = 0

        for obj in self.export_data.get("buildings", []):

            building = self.static_loader.get_building(obj["data"])

            if building is None:
                continue

            name = building["name"]

            # count = obj.get("cnt", 1)
            if "cnt" in obj:
                count = obj["cnt"]
            else:
                count = 1
                
            level = obj.get("lvl")

            if building["type"] == "Wall":
                wall_count = count

            if name == "Town Hall":
                townhall_level = level

            building_count += count

            if name not in buildings_summary:

                buildings_summary[name] = {
                    "id": building["_id"],
                    "name": name,
                    "count": 0,
                    "level": level,
                    "size": [
                        building["width"],
                        building["width"]
                    ],
                    "category": building["type"],
                    "village": building["village"]
                }

            buildings_summary[name]["count"] += count

        # -----------------------------
        # Urutkan agar lebih rapi
        # -----------------------------
        priority = [
            "Town Hall",
            "Clan Castle",
            "Eagle Artillery",
            "Monolith",
            "Scattershot",
            "Inferno Tower",
            "X-Bow",
        ]

        def sort_key(item):
            name = item["name"]
            if name in priority:
                return (0, priority.index(name))
            return (1, name)

        buildings = sorted(buildings_summary.values(), key=sort_key)

        return {
            "townhall_level": townhall_level,
            "building_count": building_count,
            "wall_count": wall_count,
            "map_size": self.MAP_SIZE,
            "buildings": buildings,
        }



