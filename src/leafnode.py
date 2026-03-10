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
        
        htmlStart = f'<{self.tag}'
        htmlStart += ''.join([f' {key}="{value}"' for key, value in self.props.items()])
        htmlStart += '>'

        return f'{htmlStart}{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props})"