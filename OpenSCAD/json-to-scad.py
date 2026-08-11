import json
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path("C:/xampp/htdocs/coc-base-designer/doc/result/1/gemini_pro_v1.json")
STATIC_DATA_FILE = Path("C:/xampp/htdocs/coc-base-designer/data/static_data.json")
OUTPUT_FILE = Path("C:/xampp/htdocs/coc-base-designer/OpenSCAD/data_layout.scad")


# ============================================================
# HELPER
# ============================================================

def scad_string(value):
    """
    Convert Python value to OpenSCAD-compatible value.
    """

    if isinstance(value, str):
        return f'"{value}"'

    if isinstance(value, bool):
        return "true" if value else "false"

    return str(value)


# ============================================================
# LOAD JSON
# ============================================================

def load_json(file_path):
    """
    Load JSON file and return its content.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)

# ============================================================
# STATIC DATA INDEX
# ============================================================

def create_building_index(static_data):
    """
    Create lookup index berdasarkan _id.

    Example:

        {
            "1000000": {
                "_id": 1000000,
                "name": "Army Camp",
                "width": 4
            },

            "1000001": {
                "_id": 1000001,
                "name": "Town Hall",
                "width": 4
            }
        }
    """

    building_index = {}

    for building in static_data.get("buildings", []):

        building_id = str(building["_id"])

        building_index[building_id] = building

    return building_index

# ============================================================
# BUILDINGS
# ============================================================

# ============================================================
# BUILDINGS
# ============================================================

def process_buildings(
    buildings,
    building_index
):
    """
    Convert LLM building data into OpenSCAD arrays.

    LLM input:

        {
            "_id": "1000001",
            "level": 13,
            "row": 20,
            "col": 20
        }

    Static data:

        {
            "_id": 1000001,
            "width": 4
        }

    Output:

        [
            "1000001",
            13,
            20,
            20,
            4
        ]

    Format:

        id, level, row, col, width
    """

    result = []

    for building in buildings:

        building_id = str(building["_id"])

        # ----------------------------------------------------
        # Lookup static data
        # ----------------------------------------------------

        static_building = building_index.get(building_id)

        if static_building is None:

            print(
                f"[WARNING] Building ID "
                f"{building_id} tidak ditemukan "
                f"di statis_data.json"
            )

            continue

        # ----------------------------------------------------
        # Get width from static data
        # ----------------------------------------------------

        width = static_building.get("width")

        if width is None:

            print(
                f"[WARNING] Building ID "
                f"{building_id} tidak memiliki width"
            )

            continue

        # ----------------------------------------------------
        # Create OpenSCAD row
        # ----------------------------------------------------

        row = [
            building_id,
            building["level"],
            building["row"],
            building["col"],
            width
        ]

        result.append(row)

    return result


# ============================================================
# WALLS
# ============================================================

def process_walls(walls):
    """
    Convert wall data into OpenSCAD arrays.

    LLM input:

        {
            "level": 1,
            "row": 6,
            "col": 6
        }

    Output:

        [
            1,
            6,
            6
        ]

    Format:

        level, row, col
    """

    result = []

    for wall in walls:

        row = [
            wall["level"],
            wall["row"],
            wall["col"]
        ]

        result.append(row)

    return result

# ============================================================
# SCAD ARRAY GENERATOR
# ============================================================

def generate_scad_array(data):

    """
    Convert Python list into OpenSCAD array.
    """

    lines = ["["]

    for row in data:

        values = ", ".join(
            scad_string(value)
            for value in row
        )

        lines.append(
            f"    [{values}],"
        )

    lines.append("]")

    return "\n".join(lines)

# ============================================================
# MAIN PREPROCESSING
# ============================================================

def preprocess():

    print("=" * 60)
    print("COC BASE DATA PREPROCESSING")
    print("=" * 60)


    # ========================================================
    # 1. LOAD LLM DATA
    # ========================================================

    print("\n[1/5] Loading LLM data...")

    llm_data = load_json(INPUT_FILE)


    # ========================================================
    # 2. LOAD STATIC DATA
    # ========================================================

    print("[2/5] Loading static data...")

    static_data = load_json(STATIC_DATA_FILE)


    # ========================================================
    # 3. CREATE BUILDING INDEX
    # ========================================================

    print("[3/5] Creating building index...")

    building_index = create_building_index(
        static_data
    )

    print(
        f"      Static buildings: "
        f"{len(building_index)}"
    )


    # ========================================================
    # 4. PROCESS DATA
    # ========================================================

    print("[4/5] Processing layout...")

    townhall_level = llm_data.get(
        "townhall_level"
    )

    buildings = process_buildings(
        llm_data.get("buildings", []),
        building_index
    )

    walls = process_walls(
        llm_data.get("walls", [])
    )


    # ========================================================
    # 5. GENERATE SCAD
    # ========================================================

    print("[5/5] Generating SCAD...")

    output = []

    output.append(
        "// ============================================================"
    )

    output.append(
        "// GENERATED DATA - DO NOT EDIT MANUALLY"
    )

    output.append(
        "// Generated by preprocess_layout.py"
    )

    output.append(
        "// ============================================================"
    )

    output.append("")


    # --------------------------------------------------------
    # Town Hall
    # --------------------------------------------------------

    output.append(
        f"townhall_level = {townhall_level};"
    )

    output.append("")


    # --------------------------------------------------------
    # Buildings
    # --------------------------------------------------------

    output.append(
        "// id, level, row, col, width"
    )

    output.append(
        "buildings = "
        + generate_scad_array(buildings)
        + ";"
    )

    output.append("")


    # --------------------------------------------------------
    # Walls
    # --------------------------------------------------------

    output.append(
        "// level, row, col"
    )

    output.append(
        "walls = "
        + generate_scad_array(walls)
        + ";"
    )

    output.append("")


    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Write output
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "\n".join(output)
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 60)
    print("PREPROCESSING SELESAI")
    print("=" * 60)

    print(f"Input LLM   : {INPUT_FILE}")
    print(f"Static Data : {STATIC_DATA_FILE}")
    print(f"Output SCAD : {OUTPUT_FILE}")

    print(f"\nTown Hall Level : {townhall_level}")
    print(f"Buildings       : {len(buildings)}")
    print(f"Walls           : {len(walls)}")

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    preprocess()
    
    