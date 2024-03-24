import re

from src.enumtypes import BlockType
from src.htmlnode import LeafNode, ParentNode
from src.textnode import text_node_to_html_node, TextNode
from src.inline_markdown import text_to_textnodes


# break down int blocks
def markdown_to_blocks(document: str) -> list[str]:
    blocks_list = []
    split_blocks = document.split("\n\n")
    for line in split_blocks:
        line = line.strip()
        if line == "":
            continue
        blocks_list.append(line)
    return blocks_list


# take each block and return html node according to its type
def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks_list = markdown_to_blocks(markdown)
    children = []
    for block in blocks_list:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)


# ParentNode("div", [children]) -> [TextNode("p", children) or Parent("div", [TextNode(grandchilren])) ]
def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return header_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.OL:
        return ol_to_html_node(block)
    if block_type == BlockType.UL:
        return ul_to_html_node(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    raise ValueError("Block type not found")


def text_to_children_nodes(text: str) -> list[TextNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        text_node = text_node_to_html_node(node)
        children.append(text_node)
    return children


def block_to_block_type(block: str) -> BlockType:
    def is_numbers_ordered(lines: list[str]) -> bool:
        for i, line in enumerate(lines):
            starts_with_number = re.search(r"^[0-9]\. ", line)

            if starts_with_number is None:
                return False
            if int(line[0]) != i + 1:
                return False
        return True

    # split block into lines
    lines_list = [b.strip() for b in block.split("\n") if b.strip() != ""]
    # strip whitesapce from block argument
    block = block.strip()
    # conditions for types
    has_heading = re.search(r"^(#{1,6}) ", block)
    has_ordered_list = is_numbers_ordered(lines_list)
    has_unordered_list = all(map(lambda x: re.search(r"^(\*|-)\s", x), lines_list))

    if has_heading and has_heading.group():
        return BlockType.HEADING
    if "```" == lines_list[0] and "```" == lines_list[-1]:
        # if "```" in block[3:] and "```" in block[:-3]:
        return BlockType.CODE
    if has_ordered_list:
        return BlockType.OL
    if has_unordered_list:
        return BlockType.UL
    if block.startswith(">"):
        return BlockType.QUOTE
    return BlockType.PARAGRAPH


def paragraph_to_html_node(block: str) -> ParentNode:
    split_lines = block.split("/n")
    lines = " ".join(split_lines)
    children = text_to_children_nodes(lines)
    return ParentNode("p", children)


def header_to_html_node(block: str) -> ParentNode:
    # find regex to remove brackets and other delimiters from block
    hashes = re.search(r"^#{1,6}", block)
    hash_count = 0
    if hashes:
        hash_count = len(hashes.group())
    h_tag = f"h{hash_count}"
    children = text_to_children_nodes(block[hash_count:].strip())
    return ParentNode(h_tag, children)


def quote_to_html_node(block: str) -> ParentNode:
    split_lines = block.split("\n")
    new_lines = []
    for line in split_lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote line")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children_nodes(content)
    return ParentNode("blockquote", children)


def code_to_html_node(block: str) -> ParentNode:
    if block[:3] == "```" and block[-3:] == "```":
        block = block[4:-3]
    text = text_to_children_nodes(block)
    return ParentNode("pre", text)


def ul_to_html_node(block: str) -> ParentNode:
    items = [
        ParentNode("li", text_to_children_nodes(item.lstrip("-* ")))
        for item in block.split("\n")
    ]
    return ParentNode("ul", items)


def ol_to_html_node(block: str) -> ParentNode:
    items = [
        ParentNode(
            "li", text_to_children_nodes(re.search(r"^[0-9]\. (.+)", item).group(1))
        )
        for item in block.split("\n")
    ]
    return ParentNode("ol", items)
