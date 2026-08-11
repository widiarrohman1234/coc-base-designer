// ============================================================
// COC BASE RENDERER
// ============================================================
// Reusable OpenSCAD renderer for Clash of Clans base layout.
//
// Coordinate system:
//   row -> Y
//   col -> X
//
// Data source:
//   Machine Learning / LLM -> JSON -> OpenSCAD
// ============================================================

// ============================================================
// CONFIGURATION
// ============================================================

GRID_SIZE       = 44;
CELL_SIZE       = 1;

GROUND_HEIGHT   = 0.5;
BUILDING_GAP    = 0;

BASE_ROTATION   = 45;


// ============================================================
// COLOR PALETTE
// ============================================================

COLOR_GROUND_A  = "#6B8E23";
COLOR_GROUND_B  = "#7FA33B";

COLOR_WALL      = "#555555";
COLOR_TOWNHALL  = "#8B4513";


// ============================================================
// GRID
// ============================================================

module grid() {

    for (x = [0 : GRID_SIZE - 1])
        for (y = [0 : GRID_SIZE - 1])

            translate([
                x * CELL_SIZE,
                y * CELL_SIZE,
                0
            ])

                if ((x + y) % 2 == 0)

                    color(COLOR_GROUND_A)
                        cube([
                            CELL_SIZE - BUILDING_GAP,
                            CELL_SIZE - BUILDING_GAP,
                            GROUND_HEIGHT
                        ]);

                else

                    color(COLOR_GROUND_B)
                        cube([
                            CELL_SIZE - BUILDING_GAP,
                            CELL_SIZE - BUILDING_GAP,
                            GROUND_HEIGHT
                        ]);
}


// ============================================================
// BUILDING POSITION
// ============================================================
//
// Converts:
//
//     row / col
//
// into:
//
//     X / Y position
//
// ============================================================

module position(row, col, z = GROUND_HEIGHT) {

    translate([
        col * CELL_SIZE,
        row * CELL_SIZE,
        z
    ])
        children();
}


// ============================================================
// TOWN HALL
// ============================================================

module buildings(
    row,
    col,
    width = 4,
    depth = 4,
    height = 1,
    level = 13
) {
    position(row, col)
        color(COLOR_TOWNHALL)
            cube([
                width * CELL_SIZE,
                depth * CELL_SIZE,
                height
            ]);
}


// ============================================================
// WALL
// ============================================================

module wall(
    row,
    col,
    width = 1,
    height = 2,
    level = 13
) {

    position(row, col)

        color(COLOR_WALL)

            cube([
                width * CELL_SIZE,
                CELL_SIZE,
                height
            ]);
}


// ============================================================
// DATA LAYOUT
// data export dari Machine learning atau model LLM
// ============================================================
include <data_layout.scad>;

// ============================================================
// BASE SCENE
// ============================================================
//
// Everything inside this module uses the same
// coordinate system and rotation.
// ============================================================

module base_scene() {
    translate([-22, -9, 0])
        rotate([0, 0, BASE_ROTATION]) {

            // ------------------------------------------
            // Ground
            // ------------------------------------------

            translate([0, -31, 0])
                grid();


            // ------------------------------------------
            // Buildings
            // ------------------------------------------

            translate([0, -31, 0]) {

                for (building = buildings) {
                    // echo(building);
                     // id, level, row, col, width
                    // Town Hall
                    buildings(
                        row = building[2],
                        col = building[3],
                        width = building[4],
                        depth = building[4], 
                        height = 4,
                        level = building[1]
                    );
                }

                for (wall_data = walls) {
                    // echo(wall_data);
                    // Wall
                    wall(
                        row = wall_data[1],
                        col = wall_data[2],
                        width = wall_data[3],
                        height = 1,
                        level = wall_data[0]
                    );
                }
              
            }
        }
}


// ============================================================
// RENDER
// ============================================================

base_scene();


