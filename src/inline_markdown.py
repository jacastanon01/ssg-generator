import re
from src.utils import TextType
from src.textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split nodes by delimiter and return a list of text nodes with the correct TextType."""
    if not isinstance(old_nodes, list):
        raise ValueError("Old nodes must be a list")

    text_type_by_delimiter = {
        "*": TextType.ITALIC,
        "**": TextType.BOLD,
        "`": TextType.CODE,
    }
    set_text_type = text_type_by_delimiter.get(delimiter, None)
    if set_text_type == None:
        raise ValueError("Delimiter must be *, ** or `")

    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"Old nodes must be list of TextNodes: {node}")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes_list = []
        split_text_nodes = node.text.split(delimiter)

        if len(split_text_nodes) % 2 == 0:
            raise ValueError("Invalid markdown")
        for i, node_text in enumerate(split_text_nodes):
            if node_text == "":
                continue
            if i % 2 == 0:
                split_nodes_list.append(TextNode(node_text, TextType.TEXT))
            else:
                split_nodes_list.append(TextNode(node_text, text_type))
        new_nodes.extend(split_nodes_list)
    return new_nodes


def extract_markdown_images(text):
    images_from_markdown = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images_from_markdown


def extract_markdown_links(text):
    links_from_markdown = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links_from_markdown