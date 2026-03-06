from enum import Enum

class TextType(Enum):
    text = "plain text"
    bold = "bold text"
    italic = "italic text"
    code = "code text"
    link = "link text"
    image = "image text"

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