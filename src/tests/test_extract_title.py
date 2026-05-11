import os
import shutil
import unittest

from generatepage import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        os.makedirs('./src/tests/temp', exist_ok=True)
        str1 = "# This is just a header"
        with open('./src/tests/temp/file1.md', 'w') as f:
            f.write(str1)
        str2 = "## h2 here\n## h3 here\n\n# all the way here for some reason"
        with open('./src/tests/temp/file2.md', 'w') as f:
            f.write(str2)
        str3 = "No h1s in here. just plain text"
        with open('./src/tests/temp/file3.md', 'w') as f:
            f.write(str3)
            
        try:
            self.assertEqual(
                extract_title('./src/tests/temp/file1.md'),
                "This is just a header"
            )
            self.assertEqual(
                extract_title('./src/tests/temp/file2.md'),
                "all the way here for some reason"
            )
            with self.assertRaises(Exception) as cm:
                extract_title('./src/tests/temp/file3.md')
        finally:
            shutil.rmtree('./src/tests/temp')