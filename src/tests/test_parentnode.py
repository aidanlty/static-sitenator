import unittest

from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode(tag="span", value="child")
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_children(self):
        parent_node = ParentNode(tag="div", children=[
            LeafNode(tag="span", value="child"),
            LeafNode(tag="span", value="child"),
            LeafNode(tag="span", value="child")
        ])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><span>child</span><span>child</span></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode(tag="b", value="grandchild")
        child_node = ParentNode(tag="span", children=[grandchild_node])
        parent_node = ParentNode(tag="div", children=[child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )
        
    def test_to_html_missing_tag_raises(self):
        child_node = LeafNode(tag="span", value='child')
        parent_node = ParentNode(tag=None, children=[child_node])
        
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
            
        self.assertEqual(str(cm.exception), f"Error: no tag attribute at {parent_node}")

    def test_to_html_missing_children_raises(self):
        child_node = LeafNode(tag="span", value='child')
        parent_node = ParentNode(tag="div", children=None)
        
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        
        self.assertEqual(str(cm.exception), f"Error: no children attribute at {parent_node}")