#!/usr/bin/env python3
"""
Python Packaging Quiz System

This script tests your knowledge of Python packaging semantics by presenting
various test cases with different project structures and import patterns.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List


class PackagingQuiz:
    def __init__(self, test_cases_dir: str = "test_cases"):
        self.test_cases_dir = Path(test_cases_dir)
        self.score = 0
        self.total_questions = 0

    def get_test_cases(self) -> List[Path]:
        """Get all test case directories."""
        if not self.test_cases_dir.exists():
            print(f"Error: Test cases directory '{self.test_cases_dir}' not found!")
            return []

        test_cases = [
            d
            for d in self.test_cases_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]
        return sorted(test_cases)

    def display_file_structure(self, test_case_dir: Path) -> None:
        """Display the file structure of a test case."""
        print(f"\n{'=' * 60}")
        print(f"TEST CASE: {test_case_dir.name}")
        print(f"{'=' * 60}")
        print("\nFile Structure:")
        print(f"{test_case_dir.name}/")

        def print_tree(path: Path, prefix: str = ""):
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}")

                if item.is_dir() and not item.name.startswith("."):
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    print_tree(item, next_prefix)

        print_tree(test_case_dir)

    def display_file_contents(self, test_case_dir: Path) -> None:
        """Display the contents of all Python files in the test case."""
        print("\nFile Contents:")
        print("-" * 40)

        def show_files(path: Path, relative_path: str = ""):
            items = sorted(path.iterdir(), key=lambda x: (x.is_dir(), x.name))
            for item in items:
                if item.name.startswith("."):
                    continue

                current_path = (
                    f"{relative_path}/{item.name}" if relative_path else item.name
                )

                if item.is_file():
                    if item.suffix == ".py" or item.name in [
                        "__init__.py",
                        "setup.py",
                        "pyproject.toml",
                    ]:
                        print(f"\n📄 {current_path}:")
                        try:
                            with open(item, "r", encoding="utf-8") as f:
                                content = f.read()
                                if content.strip():
                                    print(content)
                                else:
                                    print("(empty file)")
                        except Exception as e:
                            print(f"Error reading file: {e}")
                elif item.is_dir():
                    show_files(item, current_path)

        show_files(test_case_dir)

    def get_expected_outcome(self, test_case_dir: Path) -> Dict[str, Any]:
        """Load expected outcome from metadata file if it exists."""
        metadata_file = test_case_dir / "expected.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def run_test_case(self, test_case_dir: Path) -> Dict[str, Any]:
        """Run the test case and return the results."""
        # Create a temporary directory to run the test
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_copy = temp_path / test_case_dir.name

            # Copy the test case to temp directory
            shutil.copytree(test_case_dir, test_copy)

            # Look for the main execution file
            main_files = ["main.py", "run.py", "test.py"]
            main_file = None

            for filename in main_files:
                if (test_copy / filename).exists():
                    main_file = test_copy / filename
                    break

            if not main_file:
                return {
                    "success": False,
                    "error": "No main execution file found (main.py, run.py, or test.py)",
                    "output": "",
                    "stderr": "",
                }

            # Run the test case
            try:
                result = subprocess.run(
                    [sys.executable, str(main_file)],
                    cwd=str(test_copy),
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                return {
                    "success": result.returncode == 0,
                    "returncode": result.returncode,
                    "output": result.stdout,
                    "stderr": result.stderr,
                }

            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": "Test timed out (10 seconds)",
                    "output": "",
                    "stderr": "",
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to run test: {str(e)}",
                    "output": "",
                    "stderr": "",
                }

    def ask_prediction(self) -> str:
        """Ask user for their prediction."""
        print("\n" + "=" * 60)
        print("MAKE YOUR PREDICTION:")
        print("=" * 60)
        print("What do you think will happen when this code runs?")
        print()
        print("Options:")
        print("1. Success - Code will run without errors")
        print("2. ImportError - Module/package import will fail")
        print("3. ModuleNotFoundError - Module cannot be found")
        print("4. AttributeError - Attribute access will fail")
        print("5. SyntaxError - Code has syntax errors")
        print("6. Other error - Different type of error")
        print()

        while True:
            try:
                choice = (
                    input("Enter your prediction (1-6) or 'skip': ").strip().lower()
                )
                if choice == "skip":
                    return "skip"
                choice_num = int(choice)
                if 1 <= choice_num <= 6:
                    predictions = {
                        1: "success",
                        2: "importerror",
                        3: "modulenotfounderror",
                        4: "attributeerror",
                        5: "syntaxerror",
                        6: "other",
                    }
                    return predictions[choice_num]
                else:
                    print("Please enter a number between 1-6 or 'skip'")
            except ValueError:
                print("Please enter a valid number or 'skip'")

    def check_prediction(self, prediction: str, result: Dict[str, Any]) -> bool:
        """Check if the prediction matches the actual result."""
        if prediction == "skip":
            return False

        actual_success = result.get("success", False)
        stderr = result.get("stderr", "").lower()
        error = result.get("error", "").lower()

        if prediction == "success":
            return actual_success
        elif prediction == "importerror":
            return not actual_success and (
                "importerror" in stderr or "importerror" in error
            )
        elif prediction == "modulenotfounderror":
            return not actual_success and (
                "modulenotfounderror" in stderr or "no module named" in stderr
            )
        elif prediction == "attributeerror":
            return not actual_success and (
                "attributeerror" in stderr or "attributeerror" in error
            )
        elif prediction == "syntaxerror":
            return not actual_success and (
                "syntaxerror" in stderr or "syntaxerror" in error
            )
        elif prediction == "other":
            return not actual_success and not any(
                err in stderr
                for err in [
                    "importerror",
                    "modulenotfounderror",
                    "attributeerror",
                    "syntaxerror",
                ]
            )

        return False

    def display_result(
        self, result: Dict[str, Any], prediction: str, correct: bool
    ) -> None:
        """Display the actual result of running the test case."""
        print("\n" + "=" * 60)
        print("ACTUAL RESULT:")
        print("=" * 60)

        if result.get("success", False):
            print("✅ SUCCESS - Code executed without errors")
            if result.get("output"):
                print("\nOutput:")
                print(result["output"])
        else:
            print("❌ ERROR - Code failed to execute")

            if "error" in result:
                print(f"\nError: {result['error']}")

            if result.get("stderr"):
                print("\nError details:")
                print(result["stderr"])

            if result.get("output"):
                print("\nOutput before error:")
                print(result["output"])

        print("\n" + "-" * 40)
        if prediction != "skip":
            if correct:
                print("🎉 CORRECT! Your prediction was right!")
            else:
                print("❌ INCORRECT. Better luck next time!")
        else:
            print("⏭️  SKIPPED - No prediction made")

        input("\nPress Enter to continue...")

    def run_quiz(self) -> None:
        """Run the complete quiz."""
        print("🐍 Python Packaging Semantics Quiz")
        print("=" * 60)
        print("Test your knowledge of Python imports and packaging!")
        print()

        test_cases = self.get_test_cases()
        if not test_cases:
            print("No test cases found. Please create some test cases first.")
            return

        print(f"Found {len(test_cases)} test cases.")
        input("Press Enter to start the quiz...")

        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'=' * 20} Question {i} of {len(test_cases)} {'=' * 20}")

            # Display the test case
            self.display_file_structure(test_case)
            self.display_file_contents(test_case)

            # Get user prediction
            prediction = self.ask_prediction()

            # Run the test case
            print("\n🔄 Running test case...")
            result = self.run_test_case(test_case)

            # Check prediction and update score
            correct = self.check_prediction(prediction, result)
            if prediction != "skip":
                self.total_questions += 1
                if correct:
                    self.score += 1

            # Display result
            self.display_result(result, prediction, correct)

        # Final score
        self.display_final_score()

    def display_final_score(self) -> None:
        """Display the final quiz results."""
        print("\n" + "=" * 60)
        print("QUIZ COMPLETE!")
        print("=" * 60)

        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            print(
                f"Your Score: {self.score}/{self.total_questions} ({percentage:.1f}%)"
            )

            if percentage >= 90:
                print("🏆 Excellent! You're a Python packaging expert!")
            elif percentage >= 70:
                print(
                    "👍 Good job! You have a solid understanding of Python packaging."
                )
            elif percentage >= 50:
                print("📚 Not bad! Keep studying Python packaging concepts.")
            else:
                print("💪 Keep practicing! Python packaging can be tricky.")
        else:
            print("No questions were answered.")

        print("\nThanks for taking the quiz!")


def main():
    """Main function to run the quiz."""
    quiz = PackagingQuiz()

    try:
        quiz.run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your test cases and try again.")


if __name__ == "__main__":
    main()
