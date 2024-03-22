import re

from src.enumtypes import BlockType
from src.htmlnode import HTMLNode, LeafNode, ParentNode


def markdown_to_blocks(document: str) -> list[str]:
    blocks_list = []
    split_blocks = document.split("\n\n")

    for line in split_blocks:
        line = line.strip()
        if line == "":
            continue
        blocks_list.append(line)
    return blocks_list


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
    has_heading = re.search(r"^(#{1,6})\s+(.+?)", block)
    has_ordered_list = is_numbers_ordered(lines_list)
    has_unordered_list = all(map(lambda x: re.search(r"^(\*|-)\s", x), lines_list))

    if has_heading:
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


def block_to_leaf_node(block: str) -> LeafNode:
    pass


def block_to_html_header(block: str) -> LeafNode:
    # find regex to remove brackets and other delimiters from block
    hashes = re.search(r"^#{1,6}", block)
    hash_count = 0
    # print(f"\n########\n{block, hashes}\n#####\n")
    if block[0] == "#":
        for i in range(hashes.end()):
            hash_count += 1
    h_tag = f"h{hash_count}"
    return LeafNode(h_tag, block.lstrip("#"))


def block_to_html_quote(block: str) -> LeafNode:
    return LeafNode("blockquote", "".join(b.lstrip(">") for b in block))


def block_to_html_code(block: str) -> ParentNode:
    print(f"CODE: {block[:3]}")
    if block[:3] == "```" and block[-3:] == "```":
        block = block[3:-3]
    return ParentNode("pre", [LeafNode("code", block)])


def block_to_html_ul(block: str) -> ParentNode:
    items = [LeafNode("li", item.lstrip("-* ")) for item in block.split("\n")]
    return ParentNode("ul", items)


def block_to_html_ol(block: str) -> ParentNode:
    items = [
        LeafNode("li", re.search(r"^[0-9]\. (.+)", item).group(1))
        for item in block.split("\n")
    ]
    return ParentNode("ol", items)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks_list = markdown_to_blocks(markdown)
    print(f"++++\n{blocks_list}\n++++")
    types_of_blocks = [block_to_block_type(line) for line in blocks_list]
    html_nodes = []
    for i, block in enumerate(blocks_list):
        if [ch for ch in ["#", ">", "```", "*", "-", "1. "] if block.startswith(ch)]:
            print(f"BLOCK: {block}")
            if block[0] == "#":
                node = block_to_html_header(block)
                html_nodes.append(node)
            elif block[0] == ">":
                node = block_to_html_quote(block)
                html_nodes.append(node)
            elif block.startswith("```"):
                node = block_to_html_code(block)
                html_nodes.append(node)
            elif block.startswith(("-", "*")):
                node = block_to_html_ul(block)
                html_nodes.append(node)
            else:
                node = block_to_html_ol(block)
                html_nodes.append(node)
        else:
            # print(f"-----\n{markdown_to_blocks(block)}\n-----")
            html_nodes.append(block)
        print(f"---\n{html_nodes}\n-----")
        return HTMLNode("div", None, html_nodes)
        # LeafNode("p", block)
        # if type is quote, code or list, need a parent node
        # leaf nodes will consists on multiple i
        # print(f"******\nBlock: {block}\nType: {types_of_blocks[i]}\n****")
    parent_node = HTMLNode("div", None, None)  # Pass children nodes
