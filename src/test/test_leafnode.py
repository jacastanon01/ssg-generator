import unittest
from src.leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Some text in a paragraph!")
        node2 = LeafNode("a", "Click here", {"href": "https://google.com"})

        self.assertEqual(node.to_html(), "<p>Some text in a paragraph!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://google.com">Click here</a>')
