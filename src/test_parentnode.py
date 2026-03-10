import unittest
from leafnode import *
from parentnode import *

class test_ParentNode(unittest.TestCase):
        
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_no_tag_raises(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_no_children_raises(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_mixed_leaf_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_nested_parent_nodes(self):
        inner = ParentNode("p", [LeafNode("b", "bold")])
        outer = ParentNode("div", [inner])
        self.assertEqual(outer.to_html(), "<div><p><b>bold</b></p></div>")

    def test_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("b", "one"),
            LeafNode("i", "two"),
            LeafNode("span", "three"),
        ])
        self.assertEqual(node.to_html(), "<div><b>one</b><i>two</i><span>three</span></div>")

    def test_parent_inside_parent_inside_parent(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [LeafNode(None, "deep text")])
            ])
        ])
        self.assertEqual(node.to_html(), "<div><section><p>deep text</p></section></div>")