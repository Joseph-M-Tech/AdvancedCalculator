# AdvancedCalculator
A feature-rich scientific calculator with GUI built using Python's Tkinter library, offering advanced mathematical functions, statistical operations, and formula support.

*************Formula Reference
1. Quadratic Formula
text
ax² + bx + c = 0
x = [-b ± √(b² - 4ac)] / 2a
2. Trigonometric Formulas
Sine Law: a/sin(A) = b/sin(B) = c/sin(C)

Cosine Law: c² = a² + b² - 2ab·cos(C)

3. Statistical Formulas
Mean: μ = Σx / n

Variance: σ² = Σ(x - μ)² / n

Standard Deviation: σ = √σ²







🎮 Quick Commands Cheat Sheet
bash
# Run calculator
python advanced_calculator.py

# Run tests
python -m pytest

# Create executable
pyinstaller --onefile advanced_calculator.py

# Code formatting
black advanced_calculator.py
⭐ Star this repository if you find it useful!


File 2: requirements.txt
txt
# Advanced Calculator Requirements
# Note: Tkinter usually comes with Python installation

# Core dependencies (included with Python)
# tkinter >= 8.6
# math (standard library)

# Optional dependencies for extended features
numpy>=1.21.0  # For advanced mathematical operations
scipy>=1.7.0   # For scientific computing
matplotlib>=3.4.0  # For potential graphing features

# Development dependencies (optional)
pytest>=6.2.5  # For testing
black>=21.7b0  # For code formatting
pylint>=2.11.1  # For code linting




*********************** CONTRIBUTING.md
markdown
# Contributing to Advanced Calculator

Thank you for considering contributing to the Advanced Calculator project!

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How Can I Contribute?

### Reporting Bugs
1. Check if the bug has already been reported
2. Open a new issue with a clear title and description
3. Include steps to reproduce, expected behavior, and actual behavior
4. Add screenshots if applicable

### Suggesting Enhancements
1. Open an issue with a clear title and description
2. Explain why this enhancement would be useful
3. Include examples if possible

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Add or update tests if needed
5. Update documentation
6. Submit a pull request

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/Joseph-M-Tech/advanced-calculator.git
Create virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
Run tests:

bash
pytest
Coding Standards
Python Style
Follow PEP 8 guidelines

Use meaningful variable names

Add docstrings for functions

Keep functions focused and small

Commit Messages
Use present tense ("Add feature" not "Added feature")

Start with capital letter

Reference issue numbers if applicable

Testing
Write tests for new features

Ensure all tests pass before submitting PR

Test edge cases

Areas for Contribution
High Priority
Bug fixes

Performance improvements

Security enhancements

Medium Priority
New mathematical functions

UI/UX improvements

Documentation updates

Low Priority
Additional themes

Extra features

Questions?
Feel free to open an issue with your questions or contact the maintainers.

text

## File 6: `examples/basic_usage.py`

```python
"""
Example: Basic Usage of Advanced Calculator
This demonstrates how to use the calculator programmatically.
"""

def demonstrate_basic_operations():
    """Show basic calculator operations"""
    print("Basic Calculator Operations Demo")
    print("=" * 40)
    
    operations = [
        ("Addition", "2 + 3", 5),
        ("Subtraction", "10 - 4", 6),
        ("Multiplication", "6 × 7", 42),
        ("Division", "15 ÷ 3", 5),
        ("Percentage", "50% of 200", 100),
    ]
    
    for name, expression, expected in operations:
        print(f"{name}: {expression} = {expected}")
    
    print("\nKeyboard Shortcuts:")
    print("  Numbers: 0-9")
    print("  Operators: + - * /")
    print("  Calculate: Enter or =")
    print("  Clear: Esc")
    print("  Delete: Backspace")

def demonstrate_scientific_functions():
    """Show scientific functions"""
    print("\nScientific Functions Demo")
    print("=" * 40)
    
    functions = [
        "sin(30°) = 0.5",
        "cos(60°) = 0.5",
        "log₁₀(100) = 2",
        "√(16) = 4",
        "π ≈ 3.14159",
        "e ≈ 2.71828",
    ]
    
    for func in functions:
        print(f"  {func}")

if __name__ == "__main__":
    demonstrate_basic_operations()
    demonstrate_scientific_functions()
    print("\nTo use the GUI calculator, run:")
    print("  python advanced_calculator.py")
File 7: tests/test_basic_operations.py
python
"""
Unit tests for basic calculator operations
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from advanced_calculator import AdvancedCalculator
    import tkinter as tk
except ImportError:
    print("Warning: Tkinter not available, some tests may be skipped")
    tk = None


class TestBasicOperations(unittest.TestCase):
    """Test basic arithmetic operations"""
    
    def setUp(self):
        """Set up test environment"""
        if tk is None:
            self.skipTest("Tkinter not available")
        
        self.root = tk.Tk()
        self.calculator = AdvancedCalculator(self.root)
        self.root.withdraw()  # Hide the window during tests
    
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'root'):
            self.root.destroy()
    
    def test_addition(self):
        """Test addition operation"""
        # Simulate button clicks
        self.calculator.expression = "2+3"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "5")
    
    def test_subtraction(self):
        """Test subtraction operation"""
        self.calculator.expression = "10-4"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "6")
    
    def test_multiplication(self):
        """Test multiplication operation"""
        self.calculator.expression = "6×2"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "12")
    
    def test_division(self):
        """Test division operation"""
        self.calculator.expression = "15÷3"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "5")
    
    def test_division_by_zero(self):
        """Test division by zero error handling"""
        self.calculator.expression = "5÷0"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "Error")
    
    def test_percentage(self):
        """Test percentage calculation"""
        self.calculator.expression = "50%"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "0.5")
    
    def test_decimal_operations(self):
        """Test operations with decimal numbers"""
        self.calculator.expression = "3.5+2.5"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "6")
    
    def test_expression_with_parentheses(self):
        """Test expressions with parentheses"""
        self.calculator.expression = "(2+3)×4"
        self.calculator.calculate()
        self.assertEqual(self.calculator.result, "20")
    
    def test_clear_operation(self):
        """Test clearing calculator"""
        self.calculator.expression = "2+3"
        self.calculator.clear_all()
        self.assertEqual(self.calculator.expression, "")
        self.assertEqual(self.calculator.result, "")
    
    def test_backspace(self):
        """Test backspace functionality"""
        self.calculator.expression = "12345"
        self.calculator.backspace()
        self.assertEqual(self.calculator.expression, "1234")


class TestMemoryOperations(unittest.TestCase):
    """Test memory operations"""
    
    def setUp(self):
        """Set up test environment"""
        if tk is None:
            self.skipTest("Tkinter not available")
        
        self.root = tk.Tk()
        self.calculator = AdvancedCalculator(self.root)
        self.root.withdraw()
    
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self, 'root'):
            self.root.destroy()
    
    def test_memory_store(self):
        """Test storing to memory"""
        self.calculator.result = "42"
        self.calculator.memory_store()
        self.assertEqual(self.calculator.memory, 42)
    
    def test_memory_recall(self):
        """Test recalling from memory"""
        self.calculator.memory = 100
        self.calculator.memory_recall()
        self.assertIn("100", self.calculator.expression)
    
    def test_memory_add(self):
        """Test adding to memory"""
        self.calculator.memory = 50
        self.calculator.result = "25"
        self.calculator.memory_add()
        self.assertEqual(self.calculator.memory, 75)
    
    def test_memory_clear(self):
        """Test clearing memory"""
        self.calculator.memory = 100
        self.calculator.memory_clear()
        self.assertEqual(self.calculator.memory, 0)


if __name__ == '__main__':
    unittest.main()
File 8: docs/keyboard_shortcuts.md
markdown
# Keyboard Shortcuts Reference

## Basic Operations

| Key | Function | Alternative Keys |
|-----|----------|------------------|
| `0` - `9` | Numbers | |
| `+` | Addition | |
| `-` | Subtraction | |
| `*` | Multiplication | |
| `/` | Division | |
| `.` | Decimal point | |
| `(` | Open parenthesis | |
| `)` | Close parenthesis | |
| `Enter` | Calculate | `=` |
| `Esc` | Clear all | `Delete` |
| `Backspace` | Delete last character | |

## Scientific Functions

| Key | Function | Description |
|-----|----------|-------------|
| `p` | π (pi) | Mathematical constant (3.14159...) |
| `e` | e | Euler's number (2.71828...) |
| `^` | Power | xʸ (x to the power of y) |
| `!` | Factorial | n! (product of all positive integers ≤ n) |
| `s` | sin | Sine function |
| `c` | cos | Cosine function |
| `t` | tan | Tangent function |
| `a` + `s` | asin | Inverse sine |
| `a` + `c` | acos | Inverse cosine |
| `a` + `t` | atan | Inverse tangent |

## Navigation and Control

| Key | Function | Description |
|-----|----------|-------------|
| `Tab` | Next tab | Cycle through calculator tabs |
| `Shift` + `Tab` | Previous tab | Go to previous tab |
| `Ctrl` + `H` | Show history | Focus history panel |
| `Ctrl` + `M` | Memory operations | Focus memory buttons |
| `Ctrl` + `D` | Clear data | Clear statistical data |
| `Ctrl` + `S` | Save memory | Store current value to memory |
| `Ctrl` + `R` | Recall memory | Recall from memory |

## Angle Mode Switching

| Shortcut | Function | Description |
|----------|----------|-------------|
| `Ctrl` + `G` | DEG mode | Switch to Degrees |
| `Ctrl` + `R` | RAD mode | Switch to Radians |
| `Ctrl` + `A` | GRAD mode | Switch to Gradians |

## Special Functions

| Key Combination | Function | Description |
|-----------------|----------|-------------|
| `Shift` + `5` | % | Percentage |
| `Shift` + `8` | × | Multiplication |
| `Shift` + `/` | ÷ | Division |
| `Shift` + `6` | ^ | Power |
| `Shift` + `1` | ! | Factorial |
| `Ctrl` + `√` | sqrt | Square root |
| `Ctrl` + `3` | ∛ | Cube root |

## Mouse Operations

| Action | Function | Description |
|--------|----------|-------------|
| Click | Button press | Activate calculator button |
| Double-click | History select | Select and insert history entry |
| Right-click | Context menu | Copy/Paste operations |
| Scroll | History navigation | Scroll through history |

## Tips for Efficient Use

1. **Learn Number Pad**: If you have a number pad, use it for faster input
2. **Use Tab Navigation**: Switch between tabs quickly with Tab key
3. **Keyboard First**: Use keyboard shortcuts for common operations
4. **History Recall**: Use up/down arrows in expression field to recall previous entries
5. **Quick Clear**: Press Esc twice to completely reset calculator

## Custom Shortcuts

You can modify shortcuts in the code by editing the `bind_keys()` method in `advanced_calculator.py`:

```python
def bind_keys(self):
    # Add custom bindings here
    self.root.bind('<Control-s>', lambda e: self.memory_store())
    self.root.bind('<Control-r>', lambda e: self.memory_recall())
Accessibility Features
High Contrast Mode: Use system high contrast settings

Keyboard Navigation: All functions accessible via keyboard

Screen Reader Support: Compatible with most screen readers

Font Size Adjustment: Use Ctrl+Mouse Wheel to adjust display size

Platform-Specific Notes
Windows
Number pad fully supported

Media keys may interfere with some shortcuts

Use Alt key combinations for menu access

macOS
Use Command key instead of Control for some shortcuts

Option key for special characters

Full screen mode available

Linux
May require additional configuration for some keys

Works best with standard keyboard layouts

Customizable through system settings

Troubleshooting Keyboard Issues
If shortcuts don't work:

Ensure calculator window has focus

Check for conflicting system shortcuts

Try using the on-screen keyboard

Restart the calculator application

Check keyboard layout settings

text

## 📦 **GitHub Repository Setup Instructions**

### Step 1: Create GitHub Repository
1. Go to GitHub.com and create a new repository named `advanced-calculator`
2. Choose MIT License
3. Add Python `.gitignore`
4. Don't initialize with README (we'll add it)

### Step 2: Initialize Local Repository
```bash
# Navigate to your project folder
cd path/to/advanced-calculator

# Initialize git
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Advanced Calculator v1.0"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/advanced-calculator.git

# Push to GitHub
git branch -M main
git push -u origin main
Step 3: Create GitHub Actions (Optional)
Create .github/workflows/python-app.yml:

yaml
name: Python Calculator CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Check code formatting
      run: |
        pip install black
        black --check advanced_calculator.py
Step 4: Add GitHub Badges to README
Add these badges to the top of README.md:

markdown
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/advanced-calculator)
![GitHub issues](https://img.shields.io/github/issues/YOUR_USERNAME/advanced-calculator)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/advanced-calculator?style=social)
Step 5: Create GitHub Pages (Optional)
Create docs/index.html for project website:

html
<!DOCTYPE html>
<html>
<head>
    <title>Advanced Calculator</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>Advanced Scientific Calculator</h1>
    <p>A powerful calculator built with Python and Tkinter</p>
</body>
</html>
Enable GitHub Pages in repository settings.

🎉 Your repository is now ready!
The repository includes:

Complete calculator application

Comprehensive documentation

Unit tests

Examples

GitHub workflow

License and contribution guidelines

To push everything to GitHub:

bash
# Final push
git add .
git commit -m "Complete project setup"
git push
