from textnode import TextNode, TextType, text_node_to_html_node
from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_to_textnodes(text: str):
    
    if text == "":
        raise ValueError("String is empty")
    
    node = TextNode(text, TextType.TEXT)

    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    return new_nodes