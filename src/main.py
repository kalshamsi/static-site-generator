from textnode import *
from htmlnode import *
text_test = TextNode("This is some anchor text", TextType.link, "https://boot.dev")
htmlNode = HTMLNode('a', 'lorem ipsum', [], {'href': 'https://google.com', 'target': '_blank'})
print(htmlNode.props_to_html())