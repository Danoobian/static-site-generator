import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("wrong text type in conversion")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        elif old_node.text.count(delimiter) % 2 != 0:
            raise ValueError("unbalanced delimiters")
        else:
            parts = old_node.text.split(delimiter)
            for idx in range(len(parts)):
                if parts[idx] == "":
                    continue
                elif idx % 2:  # odd index --> True
                    new_nodes.append(TextNode(parts[idx], text_type))
                else:
                    new_nodes.append(TextNode(parts[idx], TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        found_links = extract_markdown_links(text)
        if found_links == []:
            new_nodes.append(old_node)
        else:
            while found_links != []:
                delimiter = f"[{found_links[0][0]}]({found_links[0][1]})"
                split_text = text.split(delimiter, 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(found_links[0][0], TextType.LINK, found_links[0][1])
                )
                text = split_text[1]
                found_links = extract_markdown_links(text)
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        found_images = extract_markdown_images(text)
        if found_images == []:
            new_nodes.append(old_node)
        else:
            while found_images != []:
                delimiter = f"![{found_images[0][0]}]({found_images[0][1]})"
                split_text = text.split(delimiter, 1)
                if split_text[0] != "":
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(found_images[0][0], TextType.IMAGE, found_images[0][1])
                )
                text = split_text[1]
                found_images = extract_markdown_images(text)
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    return new_nodes
