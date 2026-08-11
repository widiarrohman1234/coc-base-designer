linear_extrude(height = 5)
    text(
        "Hello World",
        size = 20,
        font = "Arial",
        halign = "center",
        valign = "center"
    );
    
translate([10,15,0])
    cube([10, 20, 5]);

translate([10,50,0])
    cylinder(h = 10, r = 5);

translate([10,70,5])
    sphere(r = 5);

translate([35,15,5])  
    cylinder(
        h = 15,
        r1 = 8,
        r2 = 1
    );    
    
linear_extrude(height = 15)    
    translate([50,15,5]) 
        polygon([
            [0, 0],
            [20, 0],
            [20, 10],
            [10, 20],
            [0, 10]
        ]);
    
translate([35,25,5])  
    rotate([0, 0, 45])
        cube([20, 10, 5]);
        
translate([-5,5,0])  
    mirror([1, 0, 0])
        cube([10, 10, 10]); 
        
translate([80,10,5])    
    union() {
        cube([20, 20, 10]);

        translate([10, 10, 10])
            sphere(r = 10);
    }
    
translate([110,10,5])         
    difference() {
        cube([30, 30, 10]);
        translate([15, 15, -1])
            cylinder(h = 12, r = 5);
    }
       
translate([145,10,5])   
    intersection() {
        cube([20, 20, 20]);
        translate([10, 10, 10])
            sphere(r = 15);
    }

translate([170,10,5])   
    for (i = [0:2]) {
        translate([i * 12, 0, 0])
            cube([10, 10, 10]);
    }




    