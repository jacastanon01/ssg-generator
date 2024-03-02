import unittest
from src.htmlnode import HTMLNode


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

        attr1 = node.props_to_attributes()
        attr2 = node2.props_to_attributes()

        self.assertEqual(node, node2)
        self.assertEqual(attr1, attr2)
        self.assertEqual(node3, node4)
        self.assertEqual(
            node.props_to_attributes(),
            ' class="rings" href="http://google.com?q=shaq+rings"',
        )


if __name__ == "__main__":
    unittest.main()
