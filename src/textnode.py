from enum import Enum
from htmlnode import *


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALICS = "italics"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, t_type, url=None):
        self.text = text
        self.text_type = t_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALICS:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return node
        case _:
            raise ValueError(f"Unkown TextType: {text_node.text_type}")