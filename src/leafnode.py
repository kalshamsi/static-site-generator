from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value, props = None):
        super().__init__(tag, value, props)

    def to_html(self):
        if self.value == None:
            raise ValueError(f'No value for leaf node {self}')
        if self.tag == None:
            return self.value
        elif self.props is not None:
            return f'<{self.tag} {self.props}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")