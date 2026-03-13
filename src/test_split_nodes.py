import unittest
from textnode import *
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link


class test_split_nodes_delimiter(unittest.TestCase):

    def test_basic_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
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

    def test_multiple_delimiters(self):
        node = TextNode("this has `code` and **bold** text, as well as __italic words__ in here", TextType.TEXT)
        code_split = split_nodes_delimiter([node], '`', TextType.CODE)
        bold_split = split_nodes_delimiter(code_split, "**", TextType.BOLD)
        italics_split = split_nodes_delimiter(bold_split, "__", TextType.ITALIC)
        self.assertEqual(italics_split, [
            TextNode("this has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text, as well as ", TextType.TEXT),
            TextNode("italic words", TextType.ITALIC),
            TextNode(" in here", TextType.TEXT),
        ])


class test_split_nodes_images(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_image_only_node(self):
        node = TextNode("![cat](https://cat.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("cat", TextType.IMAGE, "https://cat.com/cat.png")],
            new_nodes,
        )

    def test_no_images_returns_original(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_non_text_node_passes_through(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("bold text", TextType.BOLD)],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode("![cat](https://cat.com/cat.png) trailing text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("cat", TextType.IMAGE, "https://cat.com/cat.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("leading text ![cat](https://cat.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://cat.com/cat.png"),
            ],
            new_nodes,
        )

    def test_multiple_nodes_in_input(self):
        nodes = [
            TextNode("text with ![cat](https://cat.com/cat.png)", TextType.TEXT),
            TextNode("more text with ![dog](https://dog.com/dog.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("text with ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://cat.com/cat.png"),
                TextNode("more text with ", TextType.TEXT),
                TextNode("dog", TextType.IMAGE, "https://dog.com/dog.png"),
            ],
            new_nodes,
        )


class test_split_nodes_links(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_link_only_node(self):
        node = TextNode("[click here](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("click here", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_no_links_returns_original(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_non_text_node_passes_through(self):
        node = TextNode("bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("bold text", TextType.BOLD)],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode("[click here](https://example.com) trailing text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("click here", TextType.LINK, "https://example.com"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("leading text [click here](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("click here", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_image_not_treated_as_link(self):
        node = TextNode("text with ![cat](https://cat.com/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("text with ![cat](https://cat.com/cat.png)", TextType.TEXT)],
            new_nodes,
        )

    def test_multiple_nodes_in_input(self):
        nodes = [
            TextNode("text with [link one](https://one.com)", TextType.TEXT),
            TextNode("more text with [link two](https://two.com)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("text with ", TextType.TEXT),
                TextNode("link one", TextType.LINK, "https://one.com"),
                TextNode("more text with ", TextType.TEXT),
                TextNode("link two", TextType.LINK, "https://two.com"),
            ],
            new_nodes,
        )