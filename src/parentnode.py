from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError(f'No tag for parent node {self}')
        elif not self.children:
            raise ValueError(f'Parent node {self} has no children')

        htmlStart = f'<{self.tag}>'
        htmlBody = ''.join([child.to_html() for child in self.children])
        htmlEnd = f'</{self.tag}>'

        return f'{htmlStart}{htmlBody}{htmlEnd}'