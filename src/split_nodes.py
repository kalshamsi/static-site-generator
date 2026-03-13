from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []

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

def split_nodes_image(old_nodes: list):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            
        else:
            extracted_alt_url_tuples = extract_markdown_images(node.text)
            
            new_strings = node.text

            for alt_text, url in extracted_alt_url_tuples:
                new_strings = new_strings.split(f"![{alt_text}]({url})", 1)
                if len(new_strings) != 2:
                    raise ValueError("Invalid markdown: image section not closed")
                
                if new_strings[0] != "":
                    new_nodes.append(TextNode(new_strings[0], TextType.TEXT))
                
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

                new_strings = new_strings[1]

            if new_strings != "":
                new_nodes.append(TextNode(new_strings, TextType.TEXT))
                
    return new_nodes
                
def split_nodes_link(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            
        else:
            extracted_anchor_url_tuples = extract_markdown_links(node.text)
            
            new_strings = node.text

            for anchor, url in extracted_anchor_url_tuples:
                new_strings = new_strings.split(f"[{anchor}]({url})", 1)

                if len(new_strings) != 2:
                    raise ValueError("Invalid markdown: link section not closed")
                
                if new_strings[0] != "":
                    new_nodes.append(TextNode(new_strings[0], TextType.TEXT))
                
                new_nodes.append(TextNode(anchor, TextType.LINK, url))

                new_strings = new_strings[1]

            if new_strings != "":
                new_nodes.append(TextNode(new_strings, TextType.TEXT))
                
    return new_nodes

