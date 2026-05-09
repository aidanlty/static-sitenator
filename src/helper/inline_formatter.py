import re
from src.textnode import TextType, TextNode


# for BOLD, ITALIC and CODE
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    d = delimiter
    for node in old_nodes:
        if node.text_type != TextType.TEXT or d not in node.text:
            new_nodes.append(node)
        else:  # d in node.text
            node_text_list = node.text.split(d)

            if len(node_text_list) % 2 == 0:
                raise Exception(f"invalid .MD syntax, no closing {d} found")
            else:
                do_format_text = False
                for node_text in node_text_list:
                    if not node_text:
                        do_format_text = not do_format_text
                    elif not do_format_text:
                        new_nodes.append(TextNode(node_text, TextType.TEXT))
                        do_format_text = not do_format_text
                    else:
                        new_nodes.append(TextNode(node_text, text_type))
                        do_format_text = not do_format_text
    return new_nodes


# For IMAGE and LINK
def extract_markdown_images(text):
    combined_img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(combined_img_regex, text)
    return matches


def extract_markdown_links(text):
    combined_link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(combined_link_regex, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            alt_src_list = extract_markdown_images(node.text)
            if not alt_src_list:
                new_nodes.append(node)
            else:
                i = 0
                text_to_split = node.text
                while i < len(alt_src_list):
                    alt = alt_src_list[i][0]
                    src = alt_src_list[i][1]
                    md_image_phrase = f"![{alt}]({src})"

                    split = text_to_split.split(md_image_phrase, maxsplit=1)
                    if len(split) == 1:
                        if text_to_split:
                            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
                        break
                    if split[0]:
                        text_node = TextNode(split[0], TextType.TEXT)
                        new_nodes.append(text_node)
                    img_node = TextNode(alt, TextType.IMAGE, url=src)
                    new_nodes.append(img_node)
                    if not split[1]:
                        break
                    text_to_split = split[1]
                    i += 1
                else:
                    if text_to_split:
                        new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            a_href_list = extract_markdown_links(node.text)
            if not a_href_list:
                new_nodes.append(node)
            else:
                i = 0
                text_to_split = node.text
                while i < len(a_href_list):
                    a = a_href_list[i][0]
                    href = a_href_list[i][1]
                    md_link_phrase = f"[{a}]({href})"

                    split = text_to_split.split(md_link_phrase, maxsplit=1)
                    if len(split) == 1:
                        if text_to_split:
                            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
                        break
                    if split[0]:
                        text_node = TextNode(split[0], TextType.TEXT)
                        new_nodes.append(text_node)
                    link_node = TextNode(a, TextType.LINK, url=href)
                    new_nodes.append(link_node)
                    if not split[1]:
                        break
                    text_to_split = split[1]
                    i += 1
                else:
                    if text_to_split:
                        new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    """
    Example input:
        This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)
    """

    text_node = TextNode(text, TextType.TEXT)
    bold1 = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    bold2 = split_nodes_delimiter(bold1, "__", TextType.BOLD)
    italic1 = split_nodes_delimiter(bold2, "*", TextType.ITALIC)
    italic2 = split_nodes_delimiter(italic1, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic2, "`", TextType.CODE)
    image = split_nodes_image(code)
    final_text_node = split_nodes_link(image)
    return final_text_node
