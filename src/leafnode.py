from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, props = props)

    def to_html(self):
        if self.value == None:
            raise ValueError(f'No value for leaf node {self}')
        if self.tag == None:
            return self.value
        elif not self.props:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        return f'<{self.tag} {self.props}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"