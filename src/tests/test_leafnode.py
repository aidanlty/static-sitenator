import unittest
from src.leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("<h1>", "This is a leaf node", {"style": "color-red"})
        node2 = LeafNode(
            tag="<h1>", value="This is a leaf node", props={"style": "color-red"}
        )
        self.assertEqual(node, node2)

    def test_tag_not_eq(self):
        node = LeafNode("<h1>", "This is a leaf node", {"style": "color-red"})
        node2 = LeafNode(value="This is a leaf node", props={"style": "color-red"})
        self.assertNotEqual(node, node2)

    def test_value_not_eq(self):
        node = LeafNode("<h1>", "This is a leaf node", {"style": "color-red"})
        node2 = LeafNode(tag="<h1>", props={"style": "color-red"})
        self.assertNotEqual(node, node2)

    def test_props_not_eq(self):
        node = LeafNode("<h1>", "This is a leaf node", {"style": "color-red"})
        node2 = LeafNode(tag="<h1>", value="This is a leaf node", props=None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
