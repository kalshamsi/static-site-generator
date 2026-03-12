import unittest
from textnode import *
from split_nodes import split_nodes_delimiter


class test_split_nodes_delimiter(unittest.TestCase):

    def test_basic_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.CODE)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the start", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" at the start", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("text at the end `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("text at the end ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("first `code` middle `more code` end", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("first ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" middle ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("this `is not closed", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node_passes_through(self):
        node = TextNode("bold text", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("bold text", TextType.BOLD)])

    def test_mixed_text_and_non_text_nodes(self):
        nodes = [
            TextNode("normal `code` text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("normal ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
        ])

    def test_no_delimiter_in_text(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("just plain text", TextType.TEXT)])

    def test_only_delimiter_content(self):
        node = TextNode("`code only`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("code only", TextType.CODE)])

    def test_bold_delimiter(self):
        node = TextNode("this is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("this is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_empty_delimiter_content(self):
        node = TextNode("this has `` empty delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("this has ", TextType.TEXT),
            TextNode(" empty delimiters", TextType.TEXT),
        ])