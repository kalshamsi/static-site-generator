import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "Here is ![a cat](https://cat.com/cat.png)"
        self.assertEqual(extract_markdown_images(text), [
            ("a cat", "https://cat.com/cat.png")
        ])

    def test_multiple_images(self):
        text = "![a cat](https://cat.com/cat.png) and ![a dog](https://dog.com/dog.png)"
        self.assertEqual(extract_markdown_images(text), [
            ("a cat", "https://cat.com/cat.png"),
            ("a dog", "https://dog.com/dog.png"),
        ])

    def test_no_images(self):
        text = "just plain text with no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_does_not_capture_links(self):
        text = "Here is [a link](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_empty_alt_text(self):
        text = "![](https://cat.com/cat.png)"
        self.assertEqual(extract_markdown_images(text), [
            ("", "https://cat.com/cat.png")
        ])

    def test_empty_url(self):
        text = "![a cat]()"
        self.assertEqual(extract_markdown_images(text), [
            ("a cat", "")
        ])

    def test_image_and_link_mixed(self):
        text = "![a cat](https://cat.com/cat.png) and [a link](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [
            ("a cat", "https://cat.com/cat.png")
        ])


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_single_link(self):
        text = "Here is [a link](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("a link", "https://example.com")
        ])

    def test_multiple_links(self):
        text = "[first](https://first.com) and [second](https://second.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("first", "https://first.com"),
            ("second", "https://second.com"),
        ])

    def test_no_links(self):
        text = "just plain text with no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_does_not_capture_images(self):
        text = "Here is ![a cat](https://cat.com/cat.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_anchor_text(self):
        text = "[](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("", "https://example.com")
        ])

    def test_empty_url(self):
        text = "[a link]()"
        self.assertEqual(extract_markdown_links(text), [
            ("a link", "")
        ])

    def test_image_and_link_mixed(self):
        text = "![a cat](https://cat.com/cat.png) and [a link](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("a link", "https://example.com")
        ])

    def test_no_crossover_between_images_and_links(self):
        text = "![img](https://img.com) [link](https://link.com) ![img2](https://img2.com) [link2](https://link2.com)"
        self.assertEqual(extract_markdown_links(text), [
            ("link", "https://link.com"),
            ("link2", "https://link2.com"),
        ])