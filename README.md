# Python Packaging Semantics Quiz

A comprehensive quiz system to test and improve your understanding of Python packaging, imports, and module structure.

## Overview

This quiz system presents various Python packaging scenarios as test cases, shows you the code structure, asks for your predictions, and then runs the code to show you what actually happens. It's designed to help you master the intricacies of Python's import system and packaging semantics.

## How to Use

1. **Run the quiz:**
   ```bash
   python quiz.py
   ```

2. **Follow the prompts:**
   - Each test case shows you a file/folder structure
   - You'll see the contents of all Python files
   - Make your prediction about what will happen when the code runs
   - The system will execute the code and show you the actual result
   - Get immediate feedback on whether your prediction was correct

3. **Learn from the results:**
   - See detailed explanations of what happened
   - Understand why certain imports succeed or fail
   - Build intuition about Python's packaging system

## Test Cases Included

The quiz includes 13 different test cases covering various aspects of Python packaging:

### 1. Basic Import Success (`01_basic_import_success`)
- Simple module import
- Basic function and variable access
- **Expected:** Success - demonstrates fundamental import mechanics

### 2. Package with __init__.py (`02_package_with_init`)
- Traditional Python package structure
- __init__.py controlling exports
- Cross-module imports within a package
- **Expected:** Success - shows proper package organization

### 3. Missing Module Error (`03_missing_module_error`)
- Attempting to import a non-existent module
- **Expected:** ModuleNotFoundError

### 4. Import Error - Missing Function (`04_import_error_missing_function`)
- Importing a function that doesn't exist in the module
- **Expected:** ImportError

### 5. Circular Import (`05_circular_import`)
- Modules that import from each other
- Demonstrates circular dependency issues
- **Expected:** May work or fail depending on import timing

### 6. Namespace Package (`06_namespace_package`)
- Package without __init__.py (PEP 420)
- Implicit namespace packages
- **Expected:** Success - shows namespace package behavior

### 7. Relative Imports (`07_relative_imports`)
- Complex package with relative imports
- Demonstrates . and .. import syntax
- **Expected:** Success - shows proper relative import usage

### 8. Invalid Relative Import (`08_invalid_relative_import`)
- Relative imports used incorrectly
- **Expected:** ImportError or ValueError

### 9. Attribute Error (`09_attribute_error`)
- Accessing non-existent attributes on modules
- **Expected:** AttributeError

### 10. Star Import Conflicts (`10_star_import_conflicts`)
- Multiple `from module import *` statements
- Name conflicts and overwriting
- **Expected:** Success but with unexpected behavior

### 11. Syntax Error (`11_syntax_error`)
- Module with intentional syntax errors
- **Expected:** SyntaxError

### 12. Subpackage Structure (`12_subpackage_structure`)
- Complex nested package hierarchy
- Multi-level imports and cross-package dependencies
- **Expected:** Success - demonstrates enterprise-level package structure

### 13. Empty vs Missing __init__.py (`13_empty_vs_missing_init`)
- Comparison between regular and namespace packages
- **Expected:** Success - shows differences in package types

## Learning Objectives

After completing this quiz, you'll understand:

- **Import Mechanics:** How Python finds and loads modules
- **Package Types:** Regular packages vs namespace packages
- **Import Variations:** Absolute vs relative imports, star imports
- **Error Types:** Different import-related exceptions and their causes
- **Package Structure:** How to organize complex Python projects
- **Best Practices:** What to avoid and what patterns to follow

## Key Concepts Covered

### Import Types
- `import module`
- `from module import name`
- `from module import *`
- `from .module import name` (relative)
- `from ..module import name` (relative)

### Package Types
- **Regular Packages:** Directories with `__init__.py`
- **Namespace Packages:** Directories without `__init__.py` (PEP 420)

### Common Import Errors
- **ModuleNotFoundError:** Module doesn't exist
- **ImportError:** Module exists but specific name doesn't
- **AttributeError:** Accessing non-existent attributes
- **SyntaxError:** Syntax errors in imported modules
- **ValueError:** Invalid relative imports

### Package Organization Patterns
- Simple modules
- Single-level packages
- Multi-level package hierarchies
- Cross-package dependencies
- Circular import handling

## Scoring

The quiz tracks your performance:
- **90%+:** Python packaging expert! 🏆
- **70-89%:** Solid understanding 👍
- **50-69%:** Good foundation, keep studying 📚
- **<50%:** More practice needed 💪

## Tips for Success

1. **Pay attention to file structure** - The directory layout is crucial
2. **Read __init__.py files carefully** - They control what gets imported
3. **Consider import order** - Later imports can overwrite earlier ones
4. **Think about when imports are executed** - Import-time vs runtime
5. **Remember Python version differences** - Some features are version-specific

## Extending the Quiz

To add your own test cases:

1. Create a new directory in `test_cases/`
2. Add your Python files demonstrating a specific concept
3. Include a `main.py` file that will be executed
4. Optionally add an `expected.json` file with metadata

The quiz system will automatically discover and include your new test case.

## Technical Details

- **Python Version:** Requires Python 3.3+ (for namespace packages)
- **Dependencies:** None - uses only standard library
- **Execution:** Each test case runs in isolation using subprocess
- **Safety:** Tests run in temporary directories to avoid side effects

## Educational Value

This quiz system helps you:
- **Debug import issues** in real projects
- **Design better package structures** for your applications
- **Understand Python's module system** at a deep level
- **Avoid common pitfalls** in package organization
- **Prepare for Python interviews** with packaging questions

## Conclusion

Python's import and packaging system is powerful but complex. This quiz helps you build the intuition needed to work confidently with Python packages, whether you're organizing a simple script or architecting a large application.

Happy learning! 🐍