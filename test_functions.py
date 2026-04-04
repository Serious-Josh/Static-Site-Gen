import unittest
from functions import extract_title

class TestFunctions(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Tolkien Fan Club"
        self.assertEqual(extract_title(markdown), "Tolkien Fan Club")


if __name__ == "__main__":
    unittest.main()