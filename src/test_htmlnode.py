import unittest

from htmlnode import *

class test_htmlnode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "lorem ipsum")
        node2 = HTMLNode("p", 'lorem ipsum')
        self.assertEqual(node, node2)
    
    def test_repr(self):
        node = HTMLNode('p', 'lorem ipsum')
        self.assertEqual(repr(node), 'HTMLNode(tag=p, value=lorem ipsum, children=[], props={})')

    def test_props_to_html(self):
        node = HTMLNode('a', 'lorem ipsum', [], {'href': 'https://google.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), 'href="https://google.com" target="_blank"')