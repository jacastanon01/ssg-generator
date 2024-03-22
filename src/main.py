import sys

from .textnode import TextNode
from .htmlnode import HTMLNode
import src.block_markdown as bm


def main():
    with open("src/test.md", "r") as f:
        bm.markdown_to_html_node(f.read())

    print("HELLO WORLD")


if __name__ == "__main__":
    main()
