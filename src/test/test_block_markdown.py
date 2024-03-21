import unittest
from src.block_markdown import *


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
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here",
                "This is the same paragraph on a new line",
                "* This is a list",
                "* with items",
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
