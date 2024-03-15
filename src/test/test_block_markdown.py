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
