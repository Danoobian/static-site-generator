class HTMLNode:
    """
    Represents a Markdown node.
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        props_text = ""
        for prop, value in self.props.items():
            props_text += f' {prop}="{value}"'
        return props_text

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """
    Represents an HTML end node.
    """

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("leaf node must have value")
        elif self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    """
    Represents HTML parent node.
    """

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node must have tag")
        elif not self.children:
            raise ValueError("parent node must have children")
        html_text = f"<{self.tag}>"
        for child in self.children:
            html_text += child.to_html()
        html_text += f"</{self.tag}>"
        return html_text
