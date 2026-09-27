// Phyllotaxis Pattern Generator - Mistral's Version
// Based on the mathematical principles of phyllotaxis (leaf arrangement patterns in nature)
// Creates sunflower-like generative art patterns

let angle = 0;
let angleStep = 0.1;
let c = 4; // Controls the tightness of the spiral
let n = 0; // Number of points
let totalPoints = 500; // Total number of points to draw
let scaleFactor = 2; // Scaling factor for the points
let colorMode = 0; // 0 = golden, 1 = rainbow, 2 = grayscale
let bgColor = 20;

function setup() {
    createCanvas(windowWidth, windowHeight);
    angleMode(DEGREES);
    colorMode(HSB, 360, 100, 100, 1.0);
    noStroke();
    
    // Center the drawing
    translate(width / 2, height / 2);
    
    // Calculate the golden angle (137.5 degrees)
    angleStep = 137.5;
    
    // Draw all points
    for (let i = 0; i < totalPoints; i++) {
        drawPoint(i);
    }
}

function drawPoint(i) {
    // Calculate angle using golden ratio
    angle = i * angleStep;
    
    // Calculate distance from center based on square root of index
    // This creates the spiral effect
    let r = c * sqrt(i);
    
    // Convert polar to cartesian coordinates
    let x = r * cos(angle);
    let y = r * sin(angle);
    
    // Map the position to color
    let hueValue = map(angle % 360, 0, 360, 0, 360);
    
    // Size of the ellipse based on distance from center
    let pointSize = map(r, 0, width / 2, 10, 2);
    
    // Draw the point
    push();
    translate(x, y);
    
    // Color based on selected mode
    switch(colorMode) {
        case 0: // Golden color scheme
            fill(map(i, 0, totalPoints, 50, 70), 80, 90);
            break;
        case 1: // Rainbow
            fill(hueValue, 80, 90);
            break;
        case 2: // Grayscale
            fill(0, 0, map(i, 0, totalPoints, 30, 90));
            break;
    }
    
    // Draw ellipse (flower seed)
    ellipse(0, 0, pointSize);
    pop();
}

function draw() {
    // Static image - no animation needed
    noLoop();
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
    redraw();
}

// Mouse click to change color mode
function mousePressed() {
    colorMode = (colorMode + 1) % 3;
    redraw();
}

// Key press to save image
function keyPressed() {
    if (key === 's' || key === 'S') {
        saveCanvas('phyllotaxis_mistral', 'png');
    }
}
