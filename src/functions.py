import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
            
        count = 1
        parts = node.text.split(delimiter)

        #check for no closing delimiter
        if len(parts) % 2 != 1:
                raise Exception("split_nodes_delimiter: Invalid Markdown Text")
        
        for split in parts:
            if split != "":
                if count % 2 == 1:
                        new_nodes.append(TextNode(split, TextType.TEXT))
                        count += 1
                else:
                        new_nodes.append(TextNode(split, text_type))
                        count += 1 

    return new_nodes

def extract_markdown_images(text):
      return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
      return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)