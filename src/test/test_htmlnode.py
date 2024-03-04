import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            "a",
            "Google me, Chuck!",
            None,
            {"class": "rings", "href": "http://google.com?q=shaq+rings"},
        )
        node2 = HTMLNode(
            "a",
            "Google me, Chuck!",
            None,
            {"class": "rings", "href": "http://google.com?q=shaq+rings"},
        )
        node3 = HTMLNode("div", None, node, {"class": "content-box outline"})
        node4 = HTMLNode("div", None, node2, {"class": "content-box outline"})
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)

    def test_props_to_attributes(self):
        node = HTMLNode(
            "a",
            "Google me, Chuck!",
            None,
            {"class": "rings", "href": "http://google.com?q=shaq+rings"},
        )
        self.assertEqual(
            node.props_to_attributes(),
            ' class="rings" href="http://google.com?q=shaq+rings"',
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_heading(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("h1", children)
        print(f"Test parent: {node}")
        self.assertEqual(
            node.to_html(),
            "<h1><b>Bold text</b>Normal text<i>italic text</i>Normal text</h1>",
        )

    def test_to_html_grandchildren(self):
        grandchild = LeafNode("p", "Jocko")
        child = ParentNode("div", [grandchild])
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), "<section><div><p>Jocko</p></div></section>")


if __name__ == "__main__":
    unittest.main()
