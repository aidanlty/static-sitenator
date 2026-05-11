class HTMLNode:
    """
    The HTMLNode class should have 4 data members set in the constructor:

      - tag      : A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
      - value    : A string representing the value of the HTML tag (e.g. the text inside a paragraph)
      - children : A list of HTMLNode objects representing the children of this node
      - props    : A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    """

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (
                self.tag == other.tag
                and self.value == other.value
                and self.children == other.children
                and self.props == other.props
            )
        return False

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    # for child classes to override
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        res = ""
        if self.props != None:
            for k, v in self.props.items():
                res += f' {k}="{v}"'
        return res
