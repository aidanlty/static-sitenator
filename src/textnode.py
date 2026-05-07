from enum import Enum
from multiprocessing import Value
from typing import Type

from src.leafnode import LeafNode


class TextType(Enum):
    TEXT = None
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"


class TextNode:
    def __init__(self, text, text_type, url=None):
        if isinstance(text_type, TextType):
            self.text = text
            self.text_type = text_type
            self.url = url
        else:
            raise TypeError("unknown text type")

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)
    if (
        text_node.text_type == TextType.BOLD
        or text_node.text_type == TextType.ITALIC
        or text_node.text_type == TextType.CODE
    ):
        return LeafNode(tag=text_node.text_type.value, value=text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode(
            tag=text_node.text_type.value,
            value=text_node.text,
            props={"href": text_node.url},
        )
    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag=text_node.text_type.value,
            value="",
            props={"src": text_node.url, "alt": text_node.text},
        )
    raise ValueError('invalid text type')
