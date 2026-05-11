import os
import shutil
import unittest

from src.generatepage import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        os.makedirs("temp", exist_ok=True)
        str1 = "# This is just a header"
        str2 = "## h2 here\n## h3 here\n\n# all the way here for some reason"
        str3 = "No h1s in here. just plain text"

        self.assertEqual(extract_title(str1), "This is just a header")
        self.assertEqual(extract_title(str2), "all the way here for some reason")
        with self.assertRaises(Exception) as cm:
            extract_title(str3)
