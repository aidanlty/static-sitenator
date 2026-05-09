from tkinter.tix import TEXT
import unittest
from src.textnode import TextType, TextNode
from src.helper.inline_formatter import *


class TestInlineFormatter(unittest.TestCase):

    # Basic functionality
    def test_format_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.TEXT
        )
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_format_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_format_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    # Non-TEXT nodes pass through unchanged
    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    # No delimiter in text passes through unchanged
    def test_no_delimiter_in_text(self):
        node = TextNode("plain text no delimiter", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    # Unclosed delimiter raises exception
    def test_unclosed_delimiter_raises(self):
        node = TextNode("This is **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    # Multiple nodes in old_nodes
    def test_multiple_nodes(self):
        nodes = [
            TextNode("**bold**", TextType.TEXT),
            TextNode("already italic", TextType.ITALIC),
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("already italic", TextType.ITALIC),
        ]
        self.assertEqual(result, expected)

    # Following tests for images and links
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/jfKDFNn.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another image", "https://i.imgur.com/jfKDFNn.png"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_split_images_single_node(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_single_node(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            ),
            TextNode(
                "This is bolded text",
                TextType.BOLD,
            ),
            TextNode(
                "This is text with a link [to Github](https://www.github.com)!",
                TextType.TEXT,
            ),
            TextNode(
                "![third image](https://i.imgur.com/3elNhQu.png), nice",
                TextType.TEXT,
            ),
            TextNode("This is plain ol text", TextType.TEXT),
            TextNode(
                "This is no trailing text at the end: ![last image](https://i.imgur.com/NFJD3sf.png)",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is bolded text", TextType.BOLD),
                TextNode(
                    "This is text with a link [to Github](https://www.github.com)!",
                    TextType.TEXT,
                ),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(", nice", TextType.TEXT),
                TextNode("This is plain ol text", TextType.TEXT),
                TextNode("This is no trailing text at the end: ", TextType.TEXT),
                TextNode(
                    "last image", TextType.IMAGE, "https://i.imgur.com/NFJD3sf.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        nodes = [
            TextNode(
                "This is text with a link [to Instagram](https://www.instagram.com) and another link [to X](https://x.com)",
                TextType.TEXT,
            ),
            TextNode(
                "This is bolded text",
                TextType.BOLD,
            ),
            TextNode(
                "This is text with an ![image](https://i.imgur.com/3elNhQu.png)!",
                TextType.TEXT,
            ),
            TextNode(
                "[to Youtube](https://www.youtube.com), nice",
                TextType.TEXT,
            ),
            TextNode("This is plain ol text", TextType.TEXT),
            TextNode(
                "This is no trailing text at the end: last link [to Tiktok](https://www.tiktok.com)",
                TextType.TEXT,
            ),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to Instagram", TextType.LINK, "https://www.instagram.com"),
                TextNode(" and another link ", TextType.TEXT),
                TextNode("to X", TextType.LINK, "https://x.com"),
                TextNode("This is bolded text", TextType.BOLD),
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/3elNhQu.png)!",
                    TextType.TEXT,
                ),
                TextNode("to Youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(", nice", TextType.TEXT),
                TextNode("This is plain ol text", TextType.TEXT),
                TextNode(
                    "This is no trailing text at the end: last link ", TextType.TEXT
                ),
                TextNode("to Tiktok", TextType.LINK, "https://www.tiktok.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        expected_res = [
            TextNode('This is ', TextType.TEXT),
            TextNode('text', TextType.BOLD),
            TextNode(' with an ', TextType.TEXT),
            TextNode('italic', TextType.ITALIC),
            TextNode(' word and a ', TextType.TEXT),
            TextNode('code block', TextType.CODE),
            TextNode(' and an ', TextType.TEXT),
            TextNode('obi wan image', TextType.IMAGE, url='https://i.imgur.com/fJRm4Vk.jpeg'),
            TextNode(' and a ', TextType.TEXT),
            TextNode('link', TextType.LINK, url='https://boot.dev')
        ]
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, expected_res)