# Import from local module
import utils


def main():
    # Test importing functions and variables
    print("Testing basic imports...")

    # Use imported function
    greeting = utils.greet("Python")
    print(greeting)

    # Use another imported function
    result = utils.add(5, 3)
    print(f"5 + 3 = {result}")

    # Use imported variable
    print(utils.MESSAGE)

    print("All imports successful!")


if __name__ == "__main__":
    main()
