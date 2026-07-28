import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from core.constants import BUILDING_COLORS, get_sprite_path 


class BaseRenderer:

    def __init__(self, static_loader, map_size=44):
        self.loader = static_loader
        self.map_size = map_size

    # ==========================================
    # Matrix
    # ==========================================

    def create_map(self):
        return np.zeros(
            (self.map_size, self.map_size),
            dtype=int
        )

    # ==========================================
    # Placement
    # ==========================================

    def can_place(self, matrix, row, col, width, height):

        if row < 0 or col < 0:
            return False

        if row + height > matrix.shape[0]:
            return False

        if col + width > matrix.shape[1]:
            return False

        area = matrix[
            row:row+height,
            col:col+width
        ]

        return np.all(area == 0)

    def place_building(
        self,
        matrix,
        row,
        col,
        width,
        height,
        value
    ):

        matrix[
            row:row+height,
            col:col+width
        ] = value

    # ==========================================
    # Render
    # ==========================================

    def render(self, layout):
        base = self.create_map()

        annotations = []

        # -------------------------
        # Buildings
        # -------------------------
        for b in layout["buildings"]:
            building = self.loader.get_building(int(b["_id"]))

            width = building["width"]
            height = building["width"]

            self.place_building(
                base,
                b["row"],
                b["col"],
                width,
                height,
                building["_id"]
            )

            annotations.append({
                "_id": building["_id"],
                "level": b["level"],
                "text": building["name"],
                "row": b["row"],
                "col": b["col"],
                "width": width,
                "height": height
            })

        # -------------------------
        # Walls
        # -------------------------
        wall = self.loader.get_building(1000010)

        for w in layout["walls"]:

            self.place_building(
                base,
                w["row"],
                w["col"],
                wall["width"],
                wall["width"],
                wall["_id"]
            )

            annotations.append({
                "_id": wall["_id"],
                "text": "",
                "row": w["row"],
                "col": w["col"],
                "width": 1,
                "height": 1
            })

        fig, ax = self.show_map(
            base,
            annotations
        )

        return fig, ax

    # ==========================================
    # Plot
    # ==========================================

    def show_map(
        self,
        base,
        annotations=None
    ):
        fig, ax = plt.subplots(figsize=(10, 10))

        # ===================================================
        # Background
        # ===================================================
        ax.set_facecolor("#f5f5f5")

        # ===================================================
        # Grid
        # ===================================================
        ax.set_xlim(-0.5, self.map_size - 0.5)
        ax.set_ylim(self.map_size - 0.5, -0.5)

        ax.set_xticks(np.arange(self.map_size))
        ax.set_yticks(np.arange(self.map_size))

        ax.set_xticklabels(
            np.arange(self.map_size),
            fontsize=8
        )

        ax.set_yticklabels(
            np.arange(self.map_size),
            fontsize=8
        )

        ax.set_xticks(
            np.arange(-0.5, self.map_size, 1),
            minor=True
        )

        ax.set_yticks(
            np.arange(-0.5, self.map_size, 1),
            minor=True
        )

        ax.grid(
            which="minor",
            color="lightgray",
            linewidth=0.5
        )

        ax.xaxis.tick_top()

        ax.tick_params(
            which="major",
            length=0
        )

        # ===================================================
        # Buildings
        # ===================================================
        if annotations is not None:

            for ann in annotations:

                color = BUILDING_COLORS.get(
                    ann["_id"],
                    "#AAAAAA"
                )

                sprite_path = get_sprite_path(
                    ann["_id"],
                    1
                    # ann["level"] 
                )

                if sprite_path is not None:

                    image = plt.imread(sprite_path)

                    ax.imshow(
                        image,
                        extent=[
                            ann["col"] - 0.5,
                            ann["col"] + ann["width"] - 0.5,
                            ann["row"] + ann["height"] - 0.5,
                            ann["row"] - 0.5,
                        ],
                        zorder=10,
                    )

                else:
                    rect = Rectangle(
                        (
                            ann["col"] - 0.5,
                            ann["row"] - 0.5
                        ),
                        ann["width"],
                        ann["height"],
                        facecolor=color,
                        edgecolor="black",
                        linewidth=1
                    )

                    ax.add_patch(rect)

                    center_x = (
                        ann["col"]
                        + ann["width"] / 2
                        - 0.5
                    )

                    center_y = (
                        ann["row"]
                        + ann["height"] / 2
                        - 0.5
                    )

                    ax.text(
                        center_x,
                        center_y,
                        ann["text"],
                        ha="center",
                        va="center",
                        fontsize=7,
                        weight="bold",
                        color="black"
                    )

        # -------------------------
        # Walls
        # -------------------------
        wall = self.loader.get_building(1000010)

        for w in base["walls"]:

            self.place_building(
                base,
                w["row"],
                w["col"],
                wall["width"],
                wall["width"],
                wall["_id"]
            )

            annotations.append({
                "text": "W",
                "row": w["row"],
                "col": w["col"],
                "width": 1,
                "height": 1
            })

        fig, ax = self.show_map(
            base,
            annotations
        )

        plt.tight_layout()

        return fig, ax

    # ==========================================
    # Save
    # ==========================================

    def save(self, fig, filename):

        fig.savefig(
            filename,
            dpi=300,
            bbox_inches="tight"
        )

        print(f"Saved : {filename}")