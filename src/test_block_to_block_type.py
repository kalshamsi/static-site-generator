import unittest
from block import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):

    # Headings
    def test_h1_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)

    def test_h2_heading(self):
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)

    def test_h6_heading(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_heading_requires_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_seven_hashes_is_not_heading(self):
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)

    # Code
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)

    def test_code_block_multiline(self):
        self.assertEqual(block_to_block_type("```\nline one\nline two\nline three\n```"), BlockType.CODE)

    def test_code_block_missing_closing(self):
        self.assertEqual(block_to_block_type("```\ncode here"), BlockType.PARAGRAPH)

    def test_code_block_missing_opening(self):
        self.assertEqual(block_to_block_type("code here\n```"), BlockType.PARAGRAPH)

    # Quotes
    def test_single_line_quote(self):
        self.assertEqual(block_to_block_type("> this is a quote"), BlockType.QUOTE)

    def test_multiline_quote(self):
        self.assertEqual(block_to_block_type("> line one\n> line two\n> line three"), BlockType.QUOTE)

    def test_quote_without_space_after_arrow(self):
        self.assertEqual(block_to_block_type(">no space quote"), BlockType.QUOTE)

    def test_quote_one_line_missing_arrow(self):
        self.assertEqual(block_to_block_type("> line one\nline two missing arrow"), BlockType.PARAGRAPH)

    # Unordered lists
    def test_single_item_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one"), BlockType.UNORDERED_LIST)

    def test_multiline_unordered_list(self):
        self.assertEqual(block_to_block_type("- item one\n- item two\n- item three"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-no space"), BlockType.PARAGRAPH)

    def test_unordered_list_one_line_missing_dash(self):
        self.assertEqual(block_to_block_type("- item one\nitem two missing dash"), BlockType.PARAGRAPH)

    # Ordered lists
    def test_single_item_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item one"), BlockType.ORDERED_LIST)

    def test_multiline_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item one\n2. item two\n3. item three"), BlockType.ORDERED_LIST)

    def test_ordered_list_must_start_at_one(self):
        self.assertEqual(block_to_block_type("2. item one\n3. item two"), BlockType.PARAGRAPH)

    def test_ordered_list_must_increment_by_one(self):
        self.assertEqual(block_to_block_type("1. item one\n3. item two"), BlockType.PARAGRAPH)

    def test_ordered_list_missing_period(self):
        self.assertEqual(block_to_block_type("1 item one\n2 item two"), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space_after_period(self):
        self.assertEqual(block_to_block_type("1.item one\n2.item two"), BlockType.PARAGRAPH)

    # Paragraphs
    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("just a plain paragraph"), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        self.assertEqual(block_to_block_type("first line\nsecond line\nthird line"), BlockType.PARAGRAPH)

    def test_paragraph_with_inline_markdown(self):
        self.assertEqual(block_to_block_type("this has **bold** and _italic_ text"), BlockType.PARAGRAPH)
