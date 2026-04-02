import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UN_LIST = "unordered_list"
    OR_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UN_LIST
    
    ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break
    if ordered:
        return BlockType.OR_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [entry.strip() for entry in blocks if entry.strip() != ""]