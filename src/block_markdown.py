from src.utils import BlockType
import re
from src.htmlnode import HTMLNode


def markdown_to_blocks(document: str) -> list[str]:
    blocks_list = []
    split_blocks = document.split("\n")

    for line in split_blocks:
        line = line.strip()
        if line == "":
            continue
        blocks_list.append(line)
    return blocks_list


def block_to_block_type(block: str) -> BlockType:
    # split block into lines
    lines_list = [b.strip() for b in block.split("\n") if b.strip() != ""]
    # strip whitesapce from block argument
    block = block.strip()
    # conditions for types
    has_heading = re.search(r"^(#{1,6})\s+(.+?)", block)
    has_ordered_list = is_numbers_ordered(lines_list)
    has_unordered_list = all(map(lambda x: x.startswith("* "), lines_list))

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


def is_numbers_ordered(lines: list[str]) -> bool:
    for i, line in enumerate(lines):
        starts_with_number = re.search(r"^[0-9]\.( )(.?+)", line)
        print(f"line: {line, i}\nstartswith: {starts_with_number}")
        if starts_with_number is None:
            return False
        if int(line[0]) != i + 1:
            return False
    return True


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks_list = markdown_to_blocks(markdown)
