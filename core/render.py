import numpy as np
import matplotlib.pyplot as plt


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

        return fig, ax

    # ==========================================
    # Plot
    # ==========================================

    def show_map(
        self,
        base,
        annotations=None
    ):

        fig, ax = plt.subplots(
            figsize=(10, 10)
        )

        ax.imshow(
            base,
            cmap="tab20",
            origin="upper",
            interpolation="none"
        )

        # Major Tick
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

        # Minor Tick
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

        if annotations is not None:

            for ann in annotations:

                center_x = (
                    ann["col"]
                    + ann["width"]/2
                    - 0.5
                )

                center_y = (
                    ann["row"]
                    + ann["height"]/2
                    - 0.5
                )

                ax.text(
                    center_x,
                    center_y,
                    ann["text"],
                    ha="center",
                    va="center",
                    fontsize=7,
                    weight="bold"
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