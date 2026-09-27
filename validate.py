#!/usr/bin/env python3
"""
Phyllotaxis Project Validation Script
Validates project structure, files, and mobile compatibility
"""

import os
import sys
import json
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
        print(f"  ✅ {description:40s} ({size:,} bytes)")
        return True
    else:
        print(f"  ❌ {description:40s} MISSING")
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
        ('<script src="phyllotaxis.js"', "p5.js script inclusion"),
        ('<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js', "p5.js CDN"),
    ]
    
    all_passed = True
    try:
        with open('index.html', 'r') as f:
            html = f.read()
        
        for pattern, description in checks:
            if pattern in html:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} MISSING")
                all_passed = False
    except FileNotFoundError:
        print("  ❌ index.html not found")
        all_passed = False
    
    return all_passed


def validate_js_content():
    """Validate JavaScript file content"""
    print_section("JavaScript Content Validation")
    
    checks = [
        ('angleStep = 137.5', "Golden angle"),
        ('c * sqrt(i)', "Phyllotaxis formula"),
        ('isMobile', "Mobile detection"),
        ('touchStarted', "Touch event handling"),
        ('preventDefault', "Prevent default behavior"),
        ('windowResized', "Window resize handler"),
        ('changeColorMode', "Color mode switching"),
        ('saveCanvas', "Canvas saving"),
    ]
    
    all_passed = True
    try:
        with open('phyllotaxis.js', 'r') as f:
            js = f.read()
        
        for pattern, description in checks:
            if pattern in js:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} MISSING")
                all_passed = False
    except FileNotFoundError:
        print("  ❌ phyllotaxis.js not found")
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
                print(f"  ✅ {key}: {data[key] if not isinstance(data[key], dict) else '[object]'}")
            else:
                print(f"  ❌ {key} MISSING")
                all_passed = False
        
        # Check scripts
        scripts = data.get('scripts', {})
        required_scripts = ['start', 'dev', 'serve']
        for script in required_scripts:
            if script in scripts:
                print(f"  ✅ Script: {script}")
            else:
                print(f"  ❌ Script: {script} MISSING")
                all_passed = False
                
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  ❌ Error reading package.json: {e}")
        all_passed = False
    
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
                print(f"    ⚠️  {description} seems too short")
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
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description} MISSING")
                all_passed = False
        except FileNotFoundError:
            print(f"  ❌ {filepath} not found")
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
    results['docs'] = validate_documentation()
    results['mobile'] = validate_mobile_compatibility()
    
    # Summary
    print_header("Validation Summary")
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status:10s} {check.capitalize()}")
    
    print(f"\n  Result: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n  🎉 All validations passed!")
        return 0
    else:
        print("\n  ⚠️  Some validations failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
