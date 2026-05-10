import re
from enum import Enum, auto

from src.leafnode import LeafNode
from src.parentnode import ParentNode
from src.formatter.inline_formatter import text_to_textnodes
from src.textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def markdown_to_blocks(markdown):
    """
    1. split document by \n\n
    2. remove empty strings in res list
    3. strip \n from remaining strings
    """

    block_strings = markdown.split("\n\n")
    new_block_strings = []

    for block in block_strings:
        block = block.strip()
        new_block_strings.append(block)
    res = list(filter(None, new_block_strings))
    return res


def block_to_block_type(md_block: str):
    heading_re = r"#{1,6} .+"
    quoteblock_re = r"(>( )*.*\n?)+"  # multiline
    unorderedlist_re = r"(- .*\n?)+"  # multiline

    if re.fullmatch(heading_re, md_block):
        return BlockType.HEADING
    if md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE
    if re.fullmatch(quoteblock_re, md_block, flags=re.MULTILINE):
        return BlockType.QUOTE
    if re.fullmatch(unorderedlist_re, md_block, flags=re.MULTILINE):
        return BlockType.UNORDERED_LIST

    # Ordered list and Paragraph
    ordered_list = md_block.split("\n")
    for i, item in enumerate(ordered_list):
        if not item.startswith(f"{i+1}. "):
            return BlockType.PARAGRAPH
    else:
        return BlockType.ORDERED_LIST


def markdown_to_html_node(markdown):
    # Split MD into blocks
    blocks = markdown_to_blocks(markdown)
    children_res_list = []

    for block in blocks:  # block is string
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                heading_level = re.match(r"^(#{1,6})", block)  # returns #s
                assert heading_level
                text = block.split(heading_level.group(0), maxsplit=1)[1].strip()
                leaf_nodes = text_to_htmlnodes(text)
                block_node = ParentNode(
                    tag=f"h{len(heading_level.group(0))}", children=leaf_nodes
                )
                children_res_list.append(block_node)

            case BlockType.CODE:
                text = block[4:-3]
                leaf_node = LeafNode(value=text)
                code = ParentNode(tag="code", children=[leaf_node])
                pre = ParentNode(tag="pre", children=[code])
                children_res_list.append(pre)

            case BlockType.QUOTE:
                text = re.sub(r"\n?> ?", "\n", block).strip()
                leaf_nodes = text_to_htmlnodes(text)
                children_res_list.append(
                    ParentNode(tag="blockquote", children=leaf_nodes)
                )

            case BlockType.UNORDERED_LIST:
                text_list = list(filter(None, re.split(r"\n?\- ", block)))
                ul_children = []
                for text in text_list:
                    li_nodes = ParentNode(
                        tag="li", children=text_to_htmlnodes(text.strip())
                    )
                    ul_children.append(li_nodes)
                ul = ParentNode(tag="ul", children=ul_children)
                children_res_list.append(ul)

            case BlockType.ORDERED_LIST:
                text_list = list(filter(None, re.split(r"\n?\d+\. ", block)))
                ol_children = []
                for text in text_list:
                    li_nodes = ParentNode(
                        tag="li", children=text_to_htmlnodes(text.strip())
                    )
                    ol_children.append(li_nodes)
                ol = ParentNode(tag="ol", children=ol_children)
                children_res_list.append(ol)

            case BlockType.PARAGRAPH:
                text = block.replace("\n", " ").strip()
                leaf_nodes = text_to_htmlnodes(text)
                children_res_list.append(ParentNode(tag="p", children=leaf_nodes))

            case _:
                raise Exception(
                    f"Error: block ({block}, {block_type}) doesn't match a BlockType"
                )

    return ParentNode(tag="div", children=children_res_list)


# Helper function, converts text to LeafNodes
def text_to_htmlnodes(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes
