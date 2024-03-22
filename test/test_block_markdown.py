import unittest

from src.block_markdown import (
    markdown_to_blocks,
    markdown_to_html_node,
    block_to_block_type,
)
from src.enumtypes import TextType, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_split_into_blocks(self):
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
                "This is **bolded** paragraph\n        This is another paragraph with *italic* text and `code` here\n        This is the same paragraph on a new line",
                "* This is a list\n        * with items",
            ],
        )

    def test_blocks_to_block_type_with_plain_text(self):
        paragraph = "This has no special characters"
        para_type = block_to_block_type(paragraph)

        self.assertEqual(para_type, BlockType.PARAGRAPH)

    def test_blocks_to_block_type_with_heading(self):
        heading = """
        ###### Heading one
        with text
        """
        heading_none = """
        #######Invalid heading
        """
        heading_type = block_to_block_type(heading)
        text_type = block_to_block_type(heading_none)

        self.assertEqual(heading_type, BlockType.HEADING)
        self.assertEqual(text_type, BlockType.PARAGRAPH)

    def test_blocks_to_block_type_with_code(self):
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

    def test_blocks_to_block_type_with_ordered_list(self):
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

        self.assertEqual(ol_block_type, BlockType.OL)
        self.assertEqual(para_block_type, BlockType.PARAGRAPH)

    def test_blocks_to_block_type_with_unordered_list(self):
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

        self.assertEqual(ul_block_type, BlockType.UL)
        self.assertEqual(ul_dash_block_type, BlockType.UL)
        self.assertEqual(invalid_ul_block_type, BlockType.PARAGRAPH)

    def test_blocks_to_block_type_with_quote(self):
        quote_block = """>Quote
        with multiple lines
        """
        quote_type = block_to_block_type(quote_block)

        self.assertEqual(quote_type, BlockType.QUOTE)
