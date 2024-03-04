class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError()

    def props_to_attributes(self):
        if not self.props:
            return ""
        attribute_str = ""
        for attr, value in self.props.items():
            attribute_str += f' {attr}="{value}"'
        return attribute_str


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props

    def __raise_if_no_value(self):
        if self.value == None:
            raise ValueError(f"Invalid value {self.value}")

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.children}, {self.value}, {self.props})"

    def to_html(self):
        self.__raise_if_no_value()

        if self.tag == None:
            return str(self.value)

        self.props = self.props_to_attributes()
        return f"<{self.tag}{self.props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        print(f"Children: {children}")
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props
        print(f"SELF children: {self.children}")

    def __raise_if_invalid(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None:
            print(f"in raise exception: {self.children}")
            raise ValueError("ParentNode must have children to be instantiated")

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def to_html(self):
        print(f"CHILD: {self.children}")
        self.__raise_if_invalid()
        if self.props:
            self.props = self.props.props_to_attributes()
        html_str = ""
        for child in self.children:
            html_str += child.to_html()
        return f"<{self.tag}{self.props_to_attributes()}>{html_str}</{self.tag}>"
