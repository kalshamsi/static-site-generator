import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "This is a single paragraph with no blank lines"
        self.assertEqual(
            markdown_to_blocks(md),
            ["This is a single paragraph with no blank lines"],
        )

    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_excessive_newlines_between_blocks(self):
        md = "first block\n\n\n\nsecond block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["first block", "second block"],
        )

    def test_leading_and_trailing_whitespace_stripped(self):
        md = "   first block   \n\n   second block   "
        self.assertEqual(
            markdown_to_blocks(md),
            ["first block", "second block"],
        )

    def test_leading_and_trailing_newlines_in_document(self):
        md = """

first block

second block

"""
        self.assertEqual(
            markdown_to_blocks(md),
            ["first block", "second block"],
        )

    def test_multiline_block_preserved(self):
        md = """first line of block
second line of block

second block"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "first line of block\nsecond line of block",
                "second block",
            ],
        )


if __name__ == "__main__":
    unittest.main()