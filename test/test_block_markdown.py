import unittest

from src.block_markdown import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
)
from src.enumtypes import TextType, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        raw_markdown = """
This is **bolded** paragraph
This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        split_blocks = markdown_to_blocks(raw_markdown)
        self.assertEqual(
            split_blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_heading(self):
        heading = """
# Heading one

## Heading two

with text in a paragraph
        """
        heading_none = """
 ####### Invalid heading
        """
        heading_type = block_to_block_type(heading)
        text_type = block_to_block_type(heading_none)
        # html_p_node = markdown_to_html_node(heading_none)
        html_h_node = markdown_to_html_node(heading)
        print(f"*****TEST HTMLNODE HEADING*******\n{html_h_node}")

        self.assertEqual(
            html_h_node.to_html(),
            "<div><h1>Heading one</h1><h2>Heading two</h2><p>with text in a paragraph</p></div>",
        )
        # self.assertEqual(
        #     html_p_node.to_html(), "<div><p>####### Invalid heading</p></div>"
        # )
        self.assertEqual(heading_type, BlockType.HEADING)
        self.assertEqual(text_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_code(self):
        code_block = """
        ```
def codeblock(hello):
    I've prove I'm a codeblock
```
        """
        code_type = block_to_block_type(code_block)

        self.assertEqual(
            code_type,
            BlockType.CODE,
        )

    def test_block_to_ordered_list(self):
        ol_block = """
1. First things first
2. I'm the realest
        """
        invalid_numbers_ol_block = """
1. First
3. Third
        """
        ol_block_type = block_to_block_type(ol_block)
        para_block_type = block_to_block_type(invalid_numbers_ol_block)
        html_ol_node = markdown_to_html_node(ol_block)

        self.assertEqual(ol_block_type, BlockType.OL)
        self.assertEqual(para_block_type, BlockType.PARAGRAPH)

    def test_block_to_unordered_list(self):
        ul_block = """* first
* second
* third """
        invalid_ul_block = """* one
*invalid bullet point
        """
        ul_block_with_dash = """
- one
- two
        """
        ul_block_type = block_to_block_type(ul_block)
        ul_dash_block_type = block_to_block_type(ul_block_with_dash)
        invalid_ul_block_type = block_to_block_type(invalid_ul_block)
        html_ul_node = markdown_to_html_node(ul_block)

        self.assertEqual(
            html_ul_node.to_html(),
            "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>",
        )
        self.assertEqual(ul_block_type, BlockType.UL)
        self.assertEqual(ul_dash_block_type, BlockType.UL)
        self.assertEqual(invalid_ul_block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_with_quote(self):
        quote_block = """> Quote
> with multiple lines
        """
        quote_type = block_to_block_type(quote_block)

        self.assertEqual(quote_type, BlockType.QUOTE)
