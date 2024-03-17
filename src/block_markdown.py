from src.utils import BlockType
import re


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
    block = block.strip()
    has_heading = re.search(r"^(#{1,6})\s+(.+?)", block)
    print(has_heading)
    if has_heading:
        return BlockType.HEADING
    if "```" in block[3:] and "```" in block[:-3]:
        return BlockType.CODE
    return BlockType.PARAGRAPH
