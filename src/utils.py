from src.htmlnode import LeafNode
from src.textnode import TextNode
from src.enumtypes import TextType

IMAGE_FORMAT = "![{}]({})"
LINK_FORMAT = "[{}]({})"

# block_type_paragraph = "paragraph"
# block_type_heading = "heading"
# block_type_code = "code"
# block_type_quote = "quote"
# block_type_list_ul = "unordered_list"
# block_type_list_ol - "ordered_list"


def text_node_to_html_node(textnode: TextNode) -> LeafNode:
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
