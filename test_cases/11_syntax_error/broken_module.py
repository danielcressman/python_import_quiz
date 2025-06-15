def valid_function():
    """This function is syntactically correct."""
    return "This function works fine"


def broken_function(
    """This function has syntax errors - missing closing parenthesis."""
    return "This will cause a SyntaxError"


class BrokenClass
    """This class is missing a colon after the class name."""

    def __init__(self):
        self.name = "broken"

    def method_with_issue(self):
        # Missing closing quote
        message = "This string is not closed properly
        return message


def another_broken_function():
    """This function has indentation errors."""
    if True:
    print("Improper indentation")
        return "This won't work"


# Invalid dictionary syntax
config = {
    "key1": "value1"
    "key2": "value2"  # Missing comma
    "key3": "value3",
}


# Function with mismatched brackets
def calculate(x, y]:  # Opening ( but closing ]
    return x + y


# Invalid assignment
123invalid_variable = "Variables can't start with numbers"


# Unclosed list
items = ["item1", "item2", "item3"
# Missing closing bracket


# Multiple syntax errors in one line
def multi_error_function(a, b c):  # Missing comma between parameters
    result = a + + b  # Double plus operator
    return result
