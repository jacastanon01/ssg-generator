from src.enumtypes import TextType
from src.htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if (text_type == TextType.LINK or text_type == TextType.IMAGE) and not url:
            raise ValueError("Links and images must have a URL")

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
    node_text_type = textnode.text_type
    if node_text_type == TextType.TEXT:
        return LeafNode(None, textnode.text)
    if node_text_type == TextType.BOLD:
        return LeafNode("b", textnode.text)
    if node_text_type == TextType.ITALIC:
        return LeafNode("i", textnode.text)
    if node_text_type == TextType.CODE:
        return LeafNode("code", textnode.text)
    if node_text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": textnode.url, "alt": node_text_type})
    if node_text_type == TextType.LINK:
        return LeafNode("a", textnode.text, {"href": textnode.url})
    raise ValueError(f"Text type not supported: {node_text_type}")
