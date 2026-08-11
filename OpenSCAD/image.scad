// ============================================================
// CLASH OF CLANS - TOWN HALL LEVEL 1
// ============================================================
//
// Approximation based on Town_Hall1.png
//
// Footprint : 4 x 4
// Type      : Town Hall
// Level     : 1
// ============================================================


// ============================================================
// CONFIGURATION
// ============================================================

$fn = 32;

TH_WIDTH  = 4;
TH_DEPTH  = 4;

WALL_HEIGHT = 2.5;
ROOF_HEIGHT = 1.2;


// ============================================================
// COLORS
// ============================================================

WOOD_DARK   = "#4A2E1B";
WOOD        = "#65401F";
WOOD_LIGHT  = "#79502A";

ROOF        = "#F59A24";
ROOF_LIGHT  = "#FFB52E";
ROOF_DARK   = "#D87818";

STONE       = "#77706A";
STONE_DARK  = "#4F4B47";

DOOR        = "#2E1B12";


// ============================================================
// WOOD WALL
// ============================================================

module wood_wall(
    width = TH_WIDTH,
    depth = TH_DEPTH,
    height = WALL_HEIGHT
) {

    color(WOOD)
        cube([
            width,
            depth,
            height
        ]);
}


// ============================================================
// WOOD PLANKS
// ============================================================
//
// Vertical wooden planks around the building.
// ============================================================

module wood_planks(
    width = TH_WIDTH,
    depth = TH_DEPTH,
    height = WALL_HEIGHT
) {

    // ------------------------------------------
    // Front wall
    // ------------------------------------------

    for (x = [0.15 : 0.45 : width - 0.15]) {

        color(WOOD_DARK)
            translate([
                x,
                -0.01,
                0
            ])
                cube([
                    0.10,
                    0.05,
                    height
                ]);
    }


    // ------------------------------------------
    // Back wall
    // ------------------------------------------

    for (x = [0.15 : 0.45 : width - 0.15]) {

        color(WOOD_DARK)
            translate([
                x,
                depth - 0.04,
                0
            ])
                cube([
                    0.10,
                    0.05,
                    height
                ]);
    }


    // ------------------------------------------
    // Left wall
    // ------------------------------------------

    for (y = [0.15 : 0.45 : depth - 0.15]) {

        color(WOOD_DARK)
            translate([
                -0.01,
                y,
                0
            ])
                cube([
                    0.05,
                    0.10,
                    height
                ]);
    }


    // ------------------------------------------
    // Right wall
    // ------------------------------------------

    for (y = [0.15 : 0.45 : depth - 0.15]) {

        color(WOOD_DARK)
            translate([
                width - 0.04,
                y,
                0
            ])
                cube([
                    0.05,
                    0.10,
                    height
                ]);
    }
}


// ============================================================
// CORNER POSTS
// ============================================================

module corner_posts(
    width = TH_WIDTH,
    depth = TH_DEPTH,
    height = WALL_HEIGHT
) {

    positions = [
        [0, 0],
        [width - 0.25, 0],
        [0, depth - 0.25],
        [width - 0.25, depth - 0.25]
    ];

    for (p = positions) {

        color(WOOD_LIGHT)

            translate([
                p[0],
                p[1],
                0
            ])

                cube([
                    0.25,
                    0.25,
                    height
                ]);
    }
}


// ============================================================
// DOOR
// ============================================================

module door(
    width = 1,
    height = 1.5
) {

    color(DOOR)

        translate([
            (TH_WIDTH - width) / 2,
            -0.02,
            0
        ])

            cube([
                width,
                0.08,
                height
            ]);
}


// ============================================================
// ROOF
// ============================================================
//
// Hipped roof approximation.
//
// Bottom:
//      4.6 x 4.6
//
// Top:
//      1.6 x 1.6
//
// ============================================================

module roof(
    width = TH_WIDTH,
    depth = TH_DEPTH
) {

    roof_width = width + 0.6;
    roof_depth = depth + 0.6;

    top_width = 1.6;
    top_depth = 1.6;

    bottom_z = WALL_HEIGHT;
    top_z = WALL_HEIGHT + ROOF_HEIGHT;


    color(ROOF)

        polyhedron(

            points = [

                // --------------------------------------
                // Bottom
                // --------------------------------------

                [
                    -0.3,
                    -0.3,
                    bottom_z
                ],

                [
                    roof_width - 0.3,
                    -0.3,
                    bottom_z
                ],

                [
                    roof_width - 0.3,
                    roof_depth - 0.3,
                    bottom_z
                ],

                [
                    -0.3,
                    roof_depth - 0.3,
                    bottom_z
                ],


                // --------------------------------------
                // Top
                // --------------------------------------

                [
                    (roof_width - top_width) / 2 - 0.3,
                    (roof_depth - top_depth) / 2 - 0.3,
                    top_z
                ],

                [
                    (roof_width + top_width) / 2 - 0.3,
                    (roof_depth - top_depth) / 2 - 0.3,
                    top_z
                ],

                [
                    (roof_width + top_width) / 2 - 0.3,
                    (roof_depth + top_depth) / 2 - 0.3,
                    top_z
                ],

                [
                    (roof_width - top_width) / 2 - 0.3,
                    (roof_depth + top_depth) / 2 - 0.3,
                    top_z
                ]
            ],

            faces = [

                // Bottom
                [0, 1, 2, 3],

                // Front
                [0, 4, 5, 1],

                // Right
                [1, 5, 6, 2],

                // Back
                [2, 6, 7, 3],

                // Left
                [3, 7, 4, 0],

                // Top
                [4, 7, 6, 5]
            ]
        );
}


// ============================================================
// ROOF PANELS
// ============================================================
//
// Decorative roof seams.
// ============================================================

module roof_seams() {

    // Front roof seam
    color(ROOF_DARK)
        translate([
            TH_WIDTH / 2,
            -0.15,
            WALL_HEIGHT + 0.05
        ])
            rotate([
                -25,
                0,
                0
            ])
                cube([
                    0.06,
                    2.2,
                    0.04
                ]);


    // Right roof seam
    color(ROOF_DARK)
        translate([
            TH_WIDTH + 0.1,
            TH_DEPTH / 2,
            WALL_HEIGHT + 0.05
        ])
            rotate([
                0,
                25,
                0
            ])
                cube([
                    2.2,
                    0.06,
                    0.04
                ]);
}


// ============================================================
// CHIMNEY
// ============================================================

module chimney() {

    chimney_width = 0.8;
    chimney_height = 0.6;


    // Chimney body

    color(STONE)

        translate([
            TH_WIDTH / 2 - chimney_width / 2,
            TH_DEPTH / 2 - chimney_width / 2,
            WALL_HEIGHT + ROOF_HEIGHT - 0.15
        ])

            cube([
                chimney_width,
                chimney_width,
                chimney_height
            ]);


    // Dark chimney opening

    color(STONE_DARK)

        translate([
            TH_WIDTH / 2 - 0.25,
            TH_DEPTH / 2 - 0.25,
            WALL_HEIGHT + ROOF_HEIGHT + chimney_height - 0.14
        ])

            cube([
                0.5,
                0.5,
                0.05
            ]);
}


// ============================================================
// TOWN HALL LEVEL 1
// ============================================================

module townhall_level_1() {

    // ------------------------------------------
    // Main wooden building
    // ------------------------------------------

    wood_wall();


    // ------------------------------------------
    // Wooden details
    // ------------------------------------------

    wood_planks();

    corner_posts();


    // ------------------------------------------
    // Door
    // ------------------------------------------

    door();


    // ------------------------------------------
    // Roof
    // ------------------------------------------

    roof();

    roof_seams();


    // ------------------------------------------
    // Chimney
    // ------------------------------------------

    chimney();
}


// ============================================================
// RENDER
// ============================================================
translate([0,0,0])
    townhall_level_1();
    // cube([1,2,3]);