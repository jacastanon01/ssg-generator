from htmlnode import HTMLNode
from leafnode import LeafNode


class ParentNode(HTMLNode):
    def __init_(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def __raise_if_invalid(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children to be instantiated")

    def to_html(self):
        self.__raise_if_invalid()
        self.props = self.props.props_to_attributes()

        html_str = f"<{self.tag}>"
        for child in children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"
