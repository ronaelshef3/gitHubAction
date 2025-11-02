"""
unittest_standard.py

A standard, well-documented Python unittest template aimed for automation testers.
Includes examples of:
 - unit tests for pure functions
 - class / method tests
 - setup / teardown
 - parameterized-style tests using subTest
 - mocking external dependencies with unittest.mock
 - testing exceptions
 - skipping tests / expected failures
 - running tests via `python -m unittest` or directly

Adapt to your project: replace sample functions/classes with your real code or import them.
"""
import main as m
import unittest
from unittest import mock
from unittest.mock import patch

# --- Sample SUT (system under test) ------------------------------------------------
# Replace these with imports from your actual module, e.g.:
# from mypackage.math_utils import add, divide



def divide(a, b):
    """Divide with explicit ZeroDivisionError for test demonstration."""
    return a / b


class Greeter:
    def __init__(self, name_provider):
        # name_provider is a dependency we can mock in tests
        self.name_provider = name_provider

    def greet(self):
        name = self.name_provider.get_name()
        return f"Hello, {name}!"


# --- Test Cases -------------------------------------------------------------------
class TestMathFunctions(unittest.TestCase):
    """Tests for simple math functions."""

    def setUp(self):
        # Runs before each test method
        self.positive_pairs = [(1, 2, 3), (0, 0, 0), (-1, 1, 0)]

    def tearDown(self):
        # Runs after each test method (useful to release resources)
        pass

    def test_add_basic(self):
        """Basic assertions for add()."""
        for a, b, expected in self.positive_pairs:
            with self.subTest(a=a, b=b):
                result = m.add(a, b)
                self.assertEqual(result, expected, f"add({a}, {b}) should be {expected}")

    def test_divide_normal(self):
        self.assertAlmostEqual(divide(10, 2), 5.0)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)

    def test_add_property(self):
        # property-based style check: commutativity (simple)
        a, b = 7, 3
        self.assertEqual(m.add(a, b), m.add(b, a))


class TestGreeterWithMock(unittest.TestCase):
    """Tests for Greeter which depends on an external name provider.

    Demonstrates mocking with unittest.mock and verifying interactions.
    """

    def test_greet_calls_name_provider(self):
        fake_provider = mock.MagicMock()
        fake_provider.get_name.return_value = "Aharon"

        greeter = Greeter(fake_provider)
        msg = greeter.greet()

        self.assertEqual(msg, "Hello, Aharon!")
        fake_provider.get_name.assert_called_once()

    @patch.object(Greeter, 'greet')
    def test_greet_patch_example(self, mocked_greet):
        # Example how to patch a method during a test
        mocked_greet.return_value = "patched!"
        gp = Greeter(name_provider=mock.MagicMock())
        self.assertEqual(gp.greet(), "patched!")


class TestIntegrationStyle(unittest.TestCase):
    """A sample integration-style test (kept small)."""

    @unittest.skip("Skipping integration test in unit test run - long running")
    def test_integration_heavy(self):
        # Example: would call external service or DB - skipped by default
        self.assertTrue(True)

    @unittest.expectedFailure
    def test_expected_failure_example(self):
        # Marking a test as expected failure (useful when bug is known)
        self.assertEqual(1 + 1, 3)


# --- Helpers / Parameterized Example ------------------------------------------------
class TestParameterization(unittest.TestCase):
    def test_multiple_inputs(self):
        cases = [
            {"input": (2, 3), "expected": 5},
            {"input": (10, -10), "expected": 0},
            {"input": (0, 0), "expected": 0},
        ]
        for case in cases:
            a, b = case["input"]
            with self.subTest(a=a, b=b):
                self.assertEqual(m.add(a, b), case["expected"])


# --- Example of testing logging / side effects with patching -----------------------
class TestSideEffects(unittest.TestCase):

    @patch('builtins.print')
    def test_print_was_called(self, mock_print):
        # Suppose some function prints; we can assert it was called.
        print('hello')
        mock_print.assert_called_with('hello')


# --- Running tests ----------------------------------------------------------------
if __name__ == '__main__':
    # This allows running the file directly: `python unittest_standard.py`
    # For CI, prefer `python -m unittest discover` or `pytest` if used.
    unittest.main(verbosity=2)
