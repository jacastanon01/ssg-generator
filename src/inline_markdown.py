import re
import typing

from src.utils import IMAGE_FORMAT, LINK_FORMAT
from src.textnode import TextNode
from src.enumtypes import TextType

VALID_DELIMITERS = ["*", "_", "**", "`"]


def text_to_textnodes(old_text: str) -> list[TextNode]:
    """Formats a string into TextNode objects"""
    nodes = [TextNode(old_text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes(nodes, TextType.IMAGE, extract_markdown_images, IMAGE_FORMAT)
    nodes = split_nodes(nodes, TextType.LINK, extract_markdown_links, LINK_FORMAT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    return nodes


def split_nodes_delimiter(
    old_nodes: list, delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Split nodes by delimiter and return a list of text nodes with the correct TextType."""
    if not isinstance(old_nodes, list):
        raise ValueError("Old nodes must be a list")

    if delimiter not in VALID_DELIMITERS:
        raise ValueError("Delimiter must be *, ** or `")

    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"Old nodes must be list of TextNodes: {node}")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes_list = []

        is_valid_delimiters = validate_open_and_closing_delimiters(node)
        if not is_valid_delimiters:
            raise ValueError("Invalid markdown. Section not closed")

        split_text_nodes = node.text.split(delimiter)
        for i, node_text in enumerate(split_text_nodes):
            if node_text == "":
                continue
            if i % 2 == 0:
                # print(f"split text {node_text}, {i}, {text_type}")
                split_nodes_list.append(TextNode(node_text, TextType.TEXT))
            else:
                split_nodes_list.append(TextNode(node_text, text_type))
        new_nodes.extend(split_nodes_list)
    return new_nodes


def validate_open_and_closing_delimiters(textnode: TextNode) -> bool:
    """Analyze text of node to verify matching opening and closing delimiters"""
    split_text_nodes = textnode.text.split()
    stack = []

    for text in split_text_nodes:
        if text in VALID_DELIMITERS:
            if text in stack:
                stack.pop()
            else:
                stack.append(text)

    return not stack


def extract_markdown_images(text: str) -> tuple[str, str]:
    """Takes markdown and returns a tuple containing the text and link for image"""
    images_from_markdown = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images_from_markdown


def extract_markdown_links(text: str) -> tuple[str, str]:
    """Extracts text and link from markdown and returns as tuple pair"""
    links_from_markdown = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links_from_markdown


def split_nodes(
    old_nodes: list[TextNode],
    text_type: TextType,
    extract_markdown: typing.Callable[[str], tuple[str, str]],
    split_format: str,
) -> list[TextNode]:
    """Returns updated TextNodes with attributes"""
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"Text must be a TextNode: {type(node)}")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        extracted = extract_markdown(original_text)

        if len(extracted) == 0:
            new_nodes.append(node)
            continue
        for item in extracted:
            split_text = original_text.split(split_format.format(item[0], item[1]))
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image or link not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], TextType.TEXT))
            new_nodes.append(TextNode(item[0], text_type, item[1]))
            original_text = split_text[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
