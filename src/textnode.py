from src.utils import TextType


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        if (text_type == TextType.LINK or text_type == TextType.IMAGE) and not url:
            raise ValueError("Links and images must have a URL")

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Split nodes by delimiter and return a list of text nodes with the correct TextType."""
    if not isinstance(old_nodes, list):
        raise ValueError("Old nodes must be a list")

    text_type_by_delimiter = {
        "*": TextType.ITALIC,
        "**": TextType.BOLD,
        "`": TextType.CODE,
    }
    set_text_type = text_type_by_delimiter.get(delimiter, None)
    if set_text_type == None:
        raise ValueError("Delimiter must be *, ** or `")

    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode):
            raise ValueError(f"Old nodes must be list of TextNodes: {node}")

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes_list = []
        split_text_nodes = node.text.split(delimiter)

        if len(split_text_nodes) % 2 == 0:
            raise ValueError("Invalid markdown")
        for i, node_text in enumerate(split_text_nodes):
            if node_text == "":
                continue
            if i % 2 == 0:
                split_nodes_list.append(TextNode(node_text, TextType.TEXT))
            else:
                split_nodes_list.append(TextNode(node_text, text_type))
        new_nodes.extend(split_nodes_list)
    return new_nodes


# def split_nodes_delimiter(old_nodes, delimiter, text_type) -> list:
#     """Split nodes by delimiter and return a list of text nodes with the correct TextType."""
#     if not isinstance(old_nodes, list):
#         raise ValueError("Old nodes must be a list")

#     text_type_by_delimiter = {
#         "*": TextType.ITALIC,
#         "**": TextType.BOLD,
#         "`": TextType.CODE,
#     }
#     text_type = text_type_by_delimiter.get(delimiter, None)
#     if text_type == None:
#         raise ValueError("Delimiter must be *, ** or `")

#     new_node = []
#     text_from_text_nodes = []
#     for node in old_nodes:
#         if not isinstance(node, TextNode):
#             raise ValueError(f"Old nodes must be list of TextNodes: {old_nodes}")

#         split_text = node.text.split(delimiter)
#         stack = []
#         str_in_node_text = ""
#         for i, char in enumerate(node.text):
#             if char in text_type_by_delimiter:
#                 if stack[-1] == char:
#                     stack.pop()
#                 else:
#                     stack.append(char)


# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     """Split nodes by delimiter and return a list of text nodes."""
#     # VALID_DELIMITERS = ["*", "**", "`"]
#     VALID_DELIMITERS = {"*": TextType.ITALIC, "**": TextType.BOLD, "`": TextType.CODE}

#     if not isinstance(old_nodes, list):
#         raise ValueError("Old nodes must be a list")

#     if delimiter not in VALID_DELIMITERS:
#         raise ValueError("Delimiter must be *, **, or `")

#     new_nodes = []
#     split_text_nodes = []
#     text_type_by_delimiter = VALID_DELIMITERS.get(delimiter, TextType.TEXT)

#     # text_nodes_list = [TextNode(block, textnode_type) for block in split_text_nodes]
#     # return text_nodes_list
