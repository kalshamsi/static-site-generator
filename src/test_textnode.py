import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.bold)
        node2 = TextNode("This is a text node", TextType.bold)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.italic)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.italic, None)")

    def test_neq(self):
        node = TextNode("This is a text node", TextType.code)
        node2 = TextNode("This is a text node", TextType.link, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.text)
        self.assertIsNone(node.self_url)

    def test_neq_different_type(self):
        node = TextNode("This is a text node", TextType.text)
        self.assertNotEqual(node, "This is a text node")

if __name__ == '__main__':
    unittest.main()