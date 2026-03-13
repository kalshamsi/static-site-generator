import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):

    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text_only(self):
        text = "just plain text with no markdown"
        self.assertListEqual(
            [TextNode("just plain text with no markdown", TextType.TEXT)],
            text_to_textnodes(text),
        )

    def test_bold_only(self):
        text = "this is **bold** text"
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_italic_only(self):
        text = "this is _italic_ text"
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_code_only(self):
        text = "this is `code` text"
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_image_only(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertListEqual(
            [TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")],
            text_to_textnodes(text),
        )

    def test_link_only(self):
        text = "[link](https://boot.dev)"
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://boot.dev")],
            text_to_textnodes(text),
        )

    def test_multiple_bold(self):
        text = "**bold one** and **bold two**"
        self.assertListEqual(
            [
                TextNode("bold one", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold two", TextType.BOLD),
            ],
            text_to_textnodes(text),
        )

    def test_bold_and_italic(self):
        text = "**bold** and _italic_"
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes(text),
        )

    def test_image_and_link(self):
        text = "![cat](https://cat.com/cat.png) and [boot dev](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://cat.com/cat.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("")