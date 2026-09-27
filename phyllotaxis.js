// Phyllotaxis Pattern Generator - Mistral's Version
// Mobile-compatible generative art using p5.js
// Based on the mathematical principles of phyllotaxis (leaf arrangement patterns in nature)

let angle = 0;
let angleStep = 137.5; // Golden angle in degrees
let c = 4; // Controls the tightness of the spiral
let n = 0; // Number of points
let totalPoints = 500; // Total number of points to draw
let colorMode = 0; // 0 = golden, 1 = rainbow, 2 = grayscale
let bgColor = 20;
let isMobile = false;
let canvas;

function setup() {
    // Check if mobile device
    isMobile = /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    
    // Create canvas with full window dimensions
    canvas = createCanvas(windowWidth, windowHeight);
    canvas.style('display', 'block');
    canvas.style('touch-action', 'none');
    
    angleMode(DEGREES);
    colorMode(HSB, 360, 100, 100, 1.0);
    noStroke();
    
    // Prevent default touch behavior
    document.addEventListener('touchmove', function(e) {
        e.preventDefault();
    }, { passive: false });
    
    drawPhyllotaxis();
}

function drawPhyllotaxis() {
    background(bgColor);
    
    // Center the drawing
    push();
    translate(width / 2, height / 2);
    
    // Calculate optimal scaling based on screen size
    let screenSize = min(width, height);
    c = map(screenSize, 300, 1500, 2, 6);
    
    // Adjust point count for mobile (performance)
    if (isMobile && screenSize < 768) {
        totalPoints = 300; // Reduce points for better mobile performance
    } else {
        totalPoints = 500;
    }
    
    // Draw all points
    for (let i = 0; i < totalPoints; i++) {
        drawPoint(i);
    }
    
    pop();
}

function drawPoint(i) {
    // Calculate angle using golden ratio
    angle = i * angleStep;
    
    // Calculate distance from center based on square root of index
    let r = c * sqrt(i);
    
    // Convert polar to cartesian coordinates
    let x = r * cos(angle);
    let y = r * sin(angle);
    
    // Map the position to color
    let hueValue = map(angle % 360, 0, 360, 0, 360);
    
    // Size of the ellipse based on distance from center
    // Scale size for different screen sizes
    let screenScale = min(width, height) / 800;
    let pointSize = map(r, 0, width / 2, 10 * screenScale, 2 * screenScale);
    
    // Ensure minimum size for visibility
    pointSize = max(pointSize, 2);
    
    // Draw the point
    push();
    translate(x, y);
    
    // Color based on selected mode
    switch(colorMode) {
        case 0: // Golden color scheme
            fill(map(i, 0, totalPoints, 40, 65), 75, 90);
            break;
        case 1: // Rainbow
            fill(hueValue, 80, 90);
            break;
        case 2: // Grayscale
            fill(0, 0, map(i, 0, totalPoints, 40, 95));
            break;
    }
    
    // Draw ellipse (flower seed)
    ellipse(0, 0, pointSize);
    pop();
}

function draw() {
    // Static image - no animation loop
    noLoop();
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
    drawPhyllotaxis();
    updateModeText();
}

// Handle both mouse and touch for color mode change
function mousePressed() {
    changeColorMode();
}

function touchStarted() {
    changeColorMode();
    return false; // Prevent default behavior
}

function changeColorMode() {
    colorMode = (colorMode + 1) % 3;
    drawPhyllotaxis();
    updateModeText();
}

function updateModeText() {
    let modeText = document.getElementById('mode-text');
    if (modeText) {
        let modes = ['Golden', 'Rainbow', 'Grayscale'];
        modeText.textContent = modes[colorMode];
    }
}

// Key press to save image
function keyPressed() {
    if (key === 's' || key === 'S') {
        saveCanvas('phyllotaxis_mistral', 'png');
    }
}

// Initialize mode text on startup
function init() {
    updateModeText();
}

// Call init after page loads
window.addEventListener('load', init);
