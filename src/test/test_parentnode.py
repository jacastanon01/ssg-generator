import unittest
from src.parentnode import ParentNode
from src.leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_eq(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("p", children)

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
