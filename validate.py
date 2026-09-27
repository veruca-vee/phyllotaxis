#!/usr/bin/env python3
"""
Phyllotaxis Project Validation Script
Validates project structure, files, content, and actual functionality
"""

import os
import sys
import json
import re
from pathlib import Path


def print_header(text):
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}")


def print_section(text):
    print(f"\n{text}")
    print("-" * len(text))


def check_file(filepath, description):
    """Check if a file exists and is readable"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  \u2705 {description:40s} ({size:,} bytes)")
        return True
    else:
        print(f"  \u274c {description:40s} MISSING")
        return False


def validate_project_structure():
    """Validate that all required files exist"""
    print_section("Project Structure Validation")
    
    required_files = [
        ("index.html", "Main HTML file"),
        ("phyllotaxis.js", "Phyllotaxis algorithm"),
        ("README.md", "Project documentation"),
        ("CONTRIBUTING.md", "Contribution guidelines"),
        ("CODE_OF_CONDUCT.md", "Code of conduct"),
        ("LICENSE", "License file"),
        ("package.json", "Project metadata"),
        ("TESTING.md", "Testing documentation"),
        (".gitignore", "Git ignore file"),
        ("CordovaApp/www/phyllotaxis.js", "Cordova phyllotaxis.js"),
        ("CordovaApp/www/p5.js", "Bundled p5.js for offline use"),
        ("CordovaApp/config.xml", "Cordova config"),
    ]
    
    all_present = True
    for filepath, description in required_files:
        if not check_file(filepath, description):
            all_present = False
    
    return all_present


def validate_html_content():
    """Validate HTML file content"""
    print_section("HTML Content Validation")
    
    checks = [
        ('<meta name="viewport"', "Viewport meta tag"),
        ('<meta name="mobile-web-app-capable"', "Mobile web app capable"),
        ('<meta name="HandheldFriendly"', "HandheldFriendly meta tag"),
        ('touch-action', "Touch action CSS"),
        ('clamp(', "Responsive typography"),
        ('@media', "Media queries"),
        ('<script src="phyllotaxis.js"', "Phyllotaxis script inclusion"),
        ('#canvas-container', "Canvas container element"),
    ]
    
    all_passed = True
    try:
        with open('index.html', 'r') as f:
            html = f.read()
        
        for pattern, description in checks:
            if pattern in html:
                print(f"  \u2705 {description}")
            else:
                print(f"  \u274c {description} MISSING")
                all_passed = False
    except FileNotFoundError:
        print("  \u274c index.html not found")
        all_passed = False
    
    return all_passed


def validate_js_content():
    """Validate JavaScript file content - check for actual bugs"""
    print_section("JavaScript Content Validation")
    
    all_passed = True
    
    # Check main phyllotaxis.js
    for js_file in ['phyllotaxis.js', 'CordovaApp/www/phyllotaxis.js']:
        if not os.path.exists(js_file):
            print(f"  \u274c {js_file} not found")
            all_passed = False
            continue
        
        with open(js_file, 'r') as f:
            js = f.read()
        
        # Check for the colorMode variable conflict bug
        if 'let colorMode' in js:
            print(f"  \u274c {js_file}: Found 'let colorMode' - shadows p5.colorMode() function")
            all_passed = False
        elif 'let paletteMode' in js:
            print(f"  \u2705 {js_file}: Uses paletteMode (not shadowing p5.colorMode)")
        
        # Check for golden angle
        if 'angleStep = 137.5078' in js:
            print(f"  \u2705 {js_file}: Exact golden angle (137.5078)")
        elif 'angleStep = 137.5' in js:
            print(f"  \u26a0\ufe0f  {js_file}: Approximate golden angle (137.5)")
        else:
            print(f"  \u274c {js_file}: Golden angle not found")
            all_passed = False
        
        # Check for phyllotaxis formula
        if 'c * sqrt(i)' in js or 'c*sqrt(i)' in js:
            print(f"  \u2705 {js_file}: Phyllotaxis formula present")
        else:
            print(f"  \u274c {js_file}: Phyllotaxis formula missing")
            all_passed = False
        
        # Check for mobile detection
        if 'isMobile' in js:
            print(f"  \u2705 {js_file}: Mobile detection present")
        else:
            print(f"  \u274c {js_file}: Mobile detection missing")
            all_passed = False
        
        # Check for touch event handling
        if 'touchStarted' in js:
            print(f"  \u2705 {js_file}: Touch event handling present")
        else:
            print(f"  \u274c {js_file}: Touch event handling missing")
            all_passed = False
        
        # Check for preventDefault
        if 'preventDefault' in js:
            print(f"  \u2705 {js_file}: Prevent default behavior present")
        else:
            print(f"  \u274c {js_file}: Prevent default behavior missing")
            all_passed = False
        
        # Check for window resize handler
        if 'windowResized' in js:
            print(f"  \u2705 {js_file}: Window resize handler present")
        else:
            print(f"  \u274c {js_file}: Window resize handler missing")
            all_passed = False
        
        # Check for color mode switching
        if 'changeColorMode' in js:
            print(f"  \u2705 {js_file}: Color mode switching present")
        else:
            print(f"  \u274c {js_file}: Color mode switching missing")
            all_passed = False
    
    return all_passed


def validate_package_json():
    """Validate package.json content"""
    print_section("Package.json Validation")
    
    all_passed = True
    try:
        with open('package.json', 'r') as f:
            data = json.load(f)
        
        required_keys = ['name', 'version', 'description', 'scripts', 'keywords', 'author', 'license']
        for key in required_keys:
            if key in data:
                value = data[key]
                if key == 'author':
                    # Check that author is not "Mistral AI" (should be Veruca Velharin)
                    if value == 'Mistral AI':
                        print(f"  \u274c {key}: {value} (should be Veruca Velharin)")
                        all_passed = False
                    else:
                        print(f"  \u2705 {key}: {value}")
                elif not isinstance(value, dict):
                    print(f"  \u2705 {key}: {value}")
                else:
                    print(f"  \u2705 {key}: [object]")
            else:
                print(f"  \u274c {key} MISSING")
                all_passed = False
        
        # Check scripts
        scripts = data.get('scripts', {})
        required_scripts = ['start', 'dev', 'serve']
        for script in required_scripts:
            if script in scripts:
                print(f"  \u2705 Script: {script}")
            else:
                print(f"  \u274c Script: {script} MISSING")
                all_passed = False
                
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  \u274c Error reading package.json: {e}")
        all_passed = False
    
    return all_passed


def validate_cordova_config():
    """Validate Cordova configuration"""
    print_section("Cordova Configuration Validation")
    
    all_passed = True
    
    # Check config.xml
    config_path = 'CordovaApp/config.xml'
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = f.read()
        
        # Check author
        if '<author' in config:
            # Extract author name
            author_match = re.search(r'<author[^>]*>([^<]+)</author>', config)
            if author_match:
                author = author_match.group(1).strip()
                if author == 'Mistral AI':
                    print(f"  \u274c Author is 'Mistral AI' (should be Veruca Velharin)")
                    all_passed = False
                else:
                    print(f"  \u2705 Author: {author}")
            else:
                print(f"  \u26a0\ufe0f  Could not parse author from config.xml")
        
        # Check for bundled p5.js
        if '<script src="p5.js"' in config or 'src="p5.js"' in config:
            print(f"  \u2705 Uses local p5.js (offline-capable)")
        elif '<script src="https://cdnjs.cloudflare.com' in config:
            print(f"  \u26a0\ufe0f  Uses CDN p5.js (requires internet)")
        
        # Check offline capability
        p5_local = os.path.exists('CordovaApp/www/p5.js')
        if p5_local:
            print(f"  \u2705 p5.js bundled locally for offline use")
        else:
            print(f"  \u274c p5.js not bundled locally (APK needs internet)")
            all_passed = False
    else:
        print(f"  \u274c {config_path} not found")
        all_passed = False
    
    return all_passed


def validate_background_color():
    """Validate that background color matches CSS"""
    print_section("Background Color Validation")
    
    all_passed = True
    
    # Check CSS background
    css_bg = '#1a1a2e'
    
    for js_file in ['phyllotaxis.js', 'CordovaApp/www/phyllotaxis.js']:
        if not os.path.exists(js_file):
            continue
        
        with open(js_file, 'r') as f:
            js = f.read()
        
        # Check for HSB background that would be wrong
        if 'background(20)' in js:
            print(f"  \u274c {js_file}: Uses background(20) which is HSB dark gray, not {css_bg}")
            all_passed = False
        elif 'background(26, 26, 46)' in js:
            print(f"  \u2705 {js_file}: Uses RGB background matching CSS ({css_bg})")
        elif f'background("{css_bg}")' in js or f"background('{css_bg}')" in js:
            print(f"  \u2705 {js_file}: Uses background color {css_bg}")
        else:
            # Try to find any background call
            bg_match = re.search(r'background\(([^)]+)\)', js)
            if bg_match:
                bg_val = bg_match.group(1)
                print(f"  \u26a0\ufe0f  {js_file}: Uses background({bg_val}) - unclear if matches CSS")
            else:
                print(f"  \u274c {js_file}: No background call found")
                all_passed = False
    
    return all_passed


def validate_pattern_scaling():
    """Validate that pattern scaling is reasonable"""
    print_section("Pattern Scaling Validation")
    
    all_passed = True
    
    for js_file in ['phyllotaxis.js', 'CordovaApp/www/phyllotaxis.js']:
        if not os.path.exists(js_file):
            continue
        
        with open(js_file, 'r') as f:
            js = f.read()
        
        # Check for scaling formula c * sqrt(i)
        # The c value should be in a reasonable range for good visibility
        c_map_match = re.search(r'c\s*=\s*map\([^)]+\)', js)
        if c_map_match:
            c_map = c_map_match.group(0)
            print(f"  \u2705 {js_file}: {c_map}")
            # Check if the range is reasonable (4-12 is good, 2-6 is too small)
            if '2, 6' in c_map or '2,6' in c_map:
                print(f"    \u26a0\ufe0f  Warning: c range 2-6 may produce small patterns")
            elif '4, 12' in c_map or '4,12' in c_map:
                print(f"    \u2705 Good scaling range for visibility")
        else:
            print(f"  \u26a0\ufe0f  {js_file}: Could not find c scaling formula")
    
    return all_passed


def validate_documentation():
    """Validate documentation files"""
    print_section("Documentation Validation")
    
    docs = [
        ('README.md', 'Project README'),
        ('CONTRIBUTING.md', 'Contribution guidelines'),
        ('CODE_OF_CONDUCT.md', 'Code of conduct'),
        ('TESTING.md', 'Testing documentation'),
    ]
    
    all_passed = True
    for filepath, description in docs:
        if check_file(filepath, description):
            # Check minimum size
            size = os.path.getsize(filepath)
            if size < 100:
                print(f"    \u26a0\ufe0f  {description} seems too short")
        else:
            all_passed = False
    
    return all_passed


def validate_mobile_compatibility():
    """Validate mobile compatibility features"""
    print_section("Mobile Compatibility Validation")
    
    mobile_checks = [
        ('<meta name="viewport"', 'index.html', 'Viewport meta tag'),
        ('mobile-web-app-capable', 'index.html', 'Mobile web app capable'),
        ('HandheldFriendly', 'index.html', 'HandheldFriendly'),
        ('touch-action', 'index.html', 'Touch action CSS'),
        ('isMobile', 'phyllotaxis.js', 'Mobile detection'),
        ('touchStarted', 'phyllotaxis.js', 'Touch event handling'),
        ('preventDefault', 'phyllotaxis.js', 'Prevent default touch'),
        ('totalPoints = 300', 'phyllotaxis.js', 'Mobile point optimization'),
    ]
    
    all_passed = True
    for pattern, filepath, description in mobile_checks:
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            if pattern in content:
                print(f"  \u2705 {description}")
            else:
                print(f"  \u274c {description} MISSING")
                all_passed = False
        except FileNotFoundError:
            print(f"  \u274c {filepath} not found")
            all_passed = False
    
    return all_passed


def main():
    print_header("Phyllotaxis Project Validation")
    
    results = {}
    
    # Run all validations
    results['structure'] = validate_project_structure()
    results['html'] = validate_html_content()
    results['js'] = validate_js_content()
    results['package'] = validate_package_json()
    results['cordova'] = validate_cordova_config()
    results['background'] = validate_background_color()
    results['scaling'] = validate_pattern_scaling()
    results['docs'] = validate_documentation()
    results['mobile'] = validate_mobile_compatibility()
    
    # Summary
    print_header("Validation Summary")
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, passed in results.items():
        status = "\u2705 PASS" if passed else "\u274c FAIL"
        print(f"  {status:10s} {check.capitalize()}")
    
    print(f"\n  Result: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n  All validations passed!")
        return 0
    else:
        print("\n  Some validations failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
