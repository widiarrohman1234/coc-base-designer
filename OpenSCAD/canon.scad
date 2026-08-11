$fn = 48;

// =============================
// PARAMETER
// =============================
body_radius = 15;
body_length = 28;

wheel_radius = 11;
wheel_width = 5;

barrel_length = 35;
barrel_front_r = 5;
barrel_back_r = 7;

base_width = 32;
base_depth = 24;
base_height = 7;


// =============================
// BODY
// =============================
module cannon_body() {
    rotate([0,90,0])
        cylinder(
            h = body_length,
            r1 = body_radius,
            r2 = body_radius * 0.82
        );
}


// =============================
// BARREL
// =============================
module cannon_barrel() {

    // Laras utama
    rotate([0,90,0])
        cylinder(
            h = barrel_length,
            r1 = barrel_back_r,
            r2 = barrel_front_r
        );

    // Moncong laras
    translate([barrel_length,0,0])
        rotate([0,90,0])
            cylinder(
                h = 6,
                r1 = 7,
                r2 = 7
            );

    // Lubang laras
    translate([barrel_length + 5,0,0])
        rotate([0,90,0])
            cylinder(
                h = 2,
                r = 4
            );
}


// =============================
// WHEEL
// =============================
module wheel() {

    rotate([90,0,0])
        difference() {

            cylinder(
                h = wheel_width,
                r = wheel_radius
            );

            cylinder(
                h = wheel_width + 1,
                r = 4
            );
        }

    // Hub roda
    rotate([90,0,0])
        cylinder(
            h = wheel_width + 2,
            r = 5
        );
}


// =============================
// BASE
// =============================
module cannon_base() {

    // Dudukan bawah
    translate([
        -base_depth/2,
        -base_width/2,
        0
    ])
    cube([
        base_depth,
        base_width,
        base_height
    ]);

    // Dudukan melengkung
    translate([-12,0,7])
        rotate([0,90,0])
            cylinder(
                h = 24,
                r = 8,
                center = true
            );
}


// =============================
// AXLE
// =============================
module axle() {

    rotate([90,0,0])
        cylinder(
            h = 34,
            r = 3,
            center = true
        );
}


// =============================
// COMPLETE CANNON
// =============================
module cannon() {

    // Base
    cannon_base();

    // Body
    translate([0,0,20])
        cannon_body();

    // Barrel
    translate([14,0,20])
        cannon_barrel();

    // Axle
    translate([0,0,12])
        axle();

    // Left wheel
    translate([0,-18,12])
        wheel();

    // Right wheel
    translate([0,18,12])
        wheel();
}


// Render
cannon();