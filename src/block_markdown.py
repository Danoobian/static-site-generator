import re
from enum import Enum


class BlockType(Enum):
    """
    Defines Markdown block types.
    """

    PARAGRAPH = ("paragraph",)
    HEADING = ("heading",)
    CODE = ("code",)
    QUOTE = ("quote",)
    UNORDERED_LIST = ("unordered_list",)
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    """
    Convert markdown sting into a list of non-empty, stripped block of strings.
    """
    markdown_blocks = markdown.split("\n\n")
    return [
        markdown_block.strip()
        for markdown_block in markdown_blocks
        if markdown_block.strip()
    ]


def block_to_block_type(block):
    """
    Returns the type of the given Markdown block.
    """
    if re.match(r"#{1,6} ", block):
        return BlockType.HEADING
    elif re.match("^```[a-zA-Z0-9]*\n[\s\S]*\n```$", block):
        return BlockType.CODE
    elif all(re.match(r"^>\s*", line) for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(re.match(r"^\s*[-+*]\s", line) for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\s*[1-9]\d*\.\s", line) for line in block.split("\n")):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
