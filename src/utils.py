from src.htmlnode import LeafNode
from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


def text_node_to_html_node(textnode):
    node_text_type = textnode.text_type
    if node_text_type == TextType.TEXT:
        return LeafNode(None, textnode.text)
    elif node_text_type == TextType.BOLD:
        return LeafNode("b", textnode.text)
    elif node_text_type == TextType.ITALIC:
        return LeafNode("i", textnode.text)
    elif node_text_type == TextType.CODE:
        return LeafNode("code", textnode.text)
    elif node_text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": textnode.url, "alt": textnode.text})
    elif node_text_type == TextType.LINK:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    else:
        raise ValueError(f"Text type not supported: {node_text_type}")
