import re
import os
from textnode import *
from block import markdown_to_blocks, block_to_block_type, BlockType
from pathlib import Path

def markdown_to_html_node(markdown):
    #breaking down markdown doc into blocks
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        type = block_to_block_type(block)

        match(type):
            case BlockType.PARAGRAPH:
                text = " ".join(block.split("\n"))
                children = text_to_children(text)
                html_nodes.append(ParentNode("p", children))
            case BlockType.HEADING:
                count = len(block) - len(block.lstrip("#"))
                text = block[count + 1:]
                children = text_to_children(text)
                html_nodes.append(ParentNode(f"h{count}", children))
            case BlockType.CODE:
                text = block[4:-3]
                node = TextNode(text, TextType.TEXT)
                child = text_node_to_html_node(node)
                code = ParentNode("code", [child])
                html_nodes.append(ParentNode("pre", [code]))
            case BlockType.QUOTE:
                splits = block.split("\n")
                new_string = []
                for line in splits:
                    if line.startswith("> "):
                        new_string.append(line[2:])
                    else:
                        new_string.append(line[1:])
                
                text = " ".join(new_string)
                children = text_to_children(text)
                html_nodes.append(ParentNode("blockquote", children))
            case BlockType.UN_LIST:
                items = [line[2:] for line in block.split("\n")]
                list_items = []

                for item in items:
                    text = text_to_children(item)
                    list_items.append(ParentNode("li", text))
                html_nodes.append(ParentNode("ul", list_items))
            case BlockType.OR_LIST:
                items = [line.split(". ", 1)[1] for line in block.split("\n")]
                list_items = []

                for item in items:
                    text = text_to_children(item)
                    list_items.append(ParentNode("li", text))
                html_nodes.append(ParentNode("ol", list_items))

    return ParentNode("div", html_nodes)

def text_to_children(text):
     nodes = text_to_textnodes(text)
     html_nodes = []
     for node in nodes:
          html_nodes.append(text_node_to_html_node(node))
     return html_nodes

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

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
             return line[2:]
    raise Exception("extract_title: no title found")

def extract_markdown_images(text):
      return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
      return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_f = open(from_path)
    template_f = open(template_path)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dest_f = open(dest_path, "w")

    markdown = from_f.read()
    from_f.close()

    template = template_f.read()
    template_f.close()

    nodes = markdown_to_html_node(markdown)
    html = nodes.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    dest_f.write(template)
    dest_f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, Path(os.path.join(dest_dir_path, entry)).with_suffix(".html"))
        else:
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, entry))