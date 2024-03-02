from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init_(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def __raise_if_no_children(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            raise ValueError("ParentNode must have children to be instantiated")
