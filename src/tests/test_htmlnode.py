import unittest
from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "hello world", ["p", "a"], {"style": "color-red"})
        node2 = HTMLNode(
            tag="h1",
            value="hello world",
            children=["p", "a"],
            props={"style": "color-red"},
        )
        self.assertEqual(node, node2)

    def test_tag_not_eq(self):
        node = HTMLNode("h1", "hello world", ["p", "a"], {"style": "color-red"})
        node2 = HTMLNode(
            value="hello world", children=["p", "a"], props={"style": "color-red"}
        )
        self.assertNotEqual(node, node2)

    def test_value_not_eq(self):
        node = HTMLNode("h1", "hello world", ["p", "a"], {"style": "color-red"})
        node2 = HTMLNode(tag="h2", children=["p", "a"], props={"style": "color-red"})
        self.assertNotEqual(node, node2)

    def test_children_not_eq(self):
        node = HTMLNode("h1", "hello world", ["p", "a"], {"style": "color-red"})
        node2 = HTMLNode(tag="h2", value="hello world", props={"style": "color-red"})
        self.assertNotEqual(node, node2)

    def test_props_not_eq(self):
        node = HTMLNode("h1", "hello world", ["p", "a"], {"style": "color-red"})
        node2 = HTMLNode(tag="h1", value="hello world", children=["p", "a"])
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
