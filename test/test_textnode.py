import unittest

from src.textnode import TextNode
from src.enumtypes import TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("That is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node too", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.google.com")
        node2 = TextNode("This is a text node", TextType.TEXT, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_no_url(self):
        self.assertRaises(ValueError, TextNode, "text", TextType.IMAGE)


if __name__ == "__main__":
    unittest.main()
