from textnode import TextNode
from htmlnode import HTMLNode
from leafnode import LeafNode


def main():
    text = TextNode("This is a text", "bold", "http://google.com")
    html = HTMLNode("a", "Google it", None, {"href": "http://google.com"})
    leaf1 = LeafNode("p", "This is a paragraph of text.")
    leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(leaf1)


if __name__ == "__main__":
    main()
