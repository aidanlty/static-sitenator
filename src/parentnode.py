from src.htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def __eq__(self, other):
        if isinstance(other, ParentNode):
            return (
                self.tag == other.tag
                and self.children == other.children
                and self.props == other.props
            )
        return False

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
        )

    def to_html(self):
        if self.tag == None:
            raise ValueError(f"Error: no tag attribute at {self}")
        if self.children == None:
            raise ValueError(f"Error: no children attribute at {self}")
        res_start = f"<{self.tag}>"
        res_end = f"</{self.tag}>"
        res = ""
        for child in self.children:
            res += child.to_html()
        return res_start + res + res_end
