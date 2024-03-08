import unittest
from src.textnode import TextNode, split_nodes_delimiter
from src.utils import TextType


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

    def test_delim_bold(self):
        bold_node = TextNode("This is **bold** text", TextType.TEXT)
        new_text_node = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertEqual(
            new_text_node,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delim_bold2(self):
        bold_node = TextNode("This is **one** bold **two** text", TextType.TEXT)
        new_text_node = split_nodes_delimiter([bold_node], "**", TextType.BOLD)
        self.assertEqual(
            new_text_node,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
                TextNode(" bold ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delim_italic(self):
        italic_node = TextNode("One *italicized text*", TextType.TEXT)
        new_text_node = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        self.assertEqual(
            new_text_node,
            [
                TextNode("One ", TextType.TEXT),
                TextNode("italicized text", TextType.ITALIC),
            ],
        )

    def test_delim_italic2(self):
        italic_node = TextNode("One *one* Two *two* three", TextType.TEXT)
        new_text_node = split_nodes_delimiter([italic_node], "*", TextType.ITALIC)
        self.assertEqual(
            new_text_node,
            [
                TextNode("One ", TextType.TEXT),
                TextNode("one", TextType.ITALIC),
                TextNode(" Two ", TextType.TEXT),
                TextNode("two", TextType.ITALIC),
                TextNode(" three", TextType.TEXT),
            ],
        )

    def test_delim_code(self):
        code_node = TextNode("Inline `code block`", TextType.TEXT)
        new_text_node = split_nodes_delimiter([code_node], "`", TextType.CODE)
        self.assertEqual(
            new_text_node,
            [TextNode("Inline ", TextType.TEXT), TextNode("code block", TextType.CODE)],
        )

    def test_delim_all_types(self):
        nodes = [
            {
                "node": TextNode("This has **text**", TextType.TEXT),
                "type": TextType.BOLD,
            },
            {
                "node": TextNode("This has *text*", TextType.TEXT),
                "type": TextType.ITALIC,
            },
            {"node": TextNode("This has `text`", TextType.TEXT), "type": TextType.CODE},
        ]
        for textnode in nodes:
            new_text_node = split_nodes_delimiter(
                [textnode["node"]],
                (
                    f"{textnode['node'].text[-1]}*"
                    if textnode["type"] == TextType.BOLD
                    else textnode["node"].text[-1]
                ),
                textnode["type"],
            )

            self.assertEqual(
                new_text_node,
                [
                    TextNode("This has ", TextType.TEXT),
                    TextNode("text", textnode["type"]),
                ],
            )


if __name__ == "__main__":
    unittest.main()
