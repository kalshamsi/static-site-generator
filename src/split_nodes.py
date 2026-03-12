from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    new_strings = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_strings = node.text.split(delimiter)
    
            if len(new_strings) % 2 == 0:
                raise ValueError("Invalid markdown syntax: formatted section not closed")
        
            for i, sentence in enumerate(new_strings):
                if sentence != "":
                    if i % 2 == 0:
                        new_nodes.append(TextNode(sentence, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(sentence, text_type))

    return new_nodes