import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT,)
    bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    italics = split_nodes_delimiter(bold, "_", TextType.ITALICS)
    code = split_nodes_delimiter(italics, "`", TextType.CODE)
    link = split_nodes_link(code)
    images = split_nodes_images(link)
    return images

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

def split_nodes_images(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
            
        text = node.text
        images = extract_markdown_images(text)

        if not images:
             new_nodes.append(node)
             continue
        
        remaining = text

        for image_text, image_url in images:
            pattern = f"![{image_text}]({image_url})"
            parts = remaining.split(pattern, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))

            remaining = parts[1] if len(parts) > 1 else ""

        if remaining:
             new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
            
        text = node.text
        links = extract_markdown_links(text)

        if not links:
             new_nodes.append(node)
             continue
        
        remaining = text

        for link_text, link_url in links:
            pattern = f"[{link_text}]({link_url})"
            parts = remaining.split(pattern, 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            remaining = parts[1] if len(parts) > 1 else ""

        if remaining:
             new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
      return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
      return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)