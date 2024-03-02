from src.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props

    def __raise_if_no_value(self):
        if self.value == None:
            raise ValueError(f"Invalid value {self.value}")

    def to_html(self):
        self.__raise_if_no_value()

        if self.tag == None:
            return str(self.value)

        self.props = self.props_to_attributes()
        return f"<{self.tag}{self.props}>{self.value}</{self.tag}>"
