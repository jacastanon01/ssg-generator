import unittest
from src.textnode import TextNode
from src.utils import TextType
from src.inline_markdown import *


class InlineMarkdown(unittest.TestCase):
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

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/dfsdkjfd.png"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with an [link](https://google.com) and [another](https://boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link", "https://google.com"),
                ("another", "https://boot.dev"),
            ],
        )
