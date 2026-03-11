from enum import Enum
from leafnode import *

class TextType(Enum):
    TEXT = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link text"
    IMAGE = "image text"

class TextNode:
    def __init__ (self, text: str, text_type: TextType, self_url: str = None):
        self.text = text
        self.text_type = text_type
        self.self_url = self_url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.self_url == other.self_url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.self_url})"
    
def text_node_to_html_node(text_node):
    if not isinstance(text_node.text_type, TextType):
        raise Exception(f"invalid text node type for text node {text_node}")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text, None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text, None)
    if text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text, None)
    if text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.self_url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode('img', "", {'src': text_node.self_url, 'alt': text_node.text})