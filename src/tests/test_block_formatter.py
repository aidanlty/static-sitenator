import textwrap
import unittest
from src.formatter.block_formatter import *


class TestBlockFormatter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """).strip()
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_successive_newlines(self):
        md = textwrap.dedent("""
            This is **bolded** paragraph


            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line






            - This is a list
            - with items
        """).strip()
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocktype_paragraph(self):
        text = textwrap.dedent("""
            This is a generic paragraph with no MD formatting.
            There's even a cheeky little single newline.
        """).strip()
        res = block_to_block_type(text)
        self.assertEqual(res, BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        text = textwrap.dedent("""
            ```
            This text should be in a code block.
            ```
        """).strip()
        res = block_to_block_type(text)
        self.assertEqual(res, BlockType.CODE)

    def test_blocktype_quote(self):
        text = textwrap.dedent("""
            > This is a quote block.
            >Here's a generous second line for you.
        """).strip()
        res = block_to_block_type(text)
        self.assertEqual(res, BlockType.QUOTE)

    def test_blocktype_unordered_list(self):
        text = textwrap.dedent("""
            - List item 1
            - List item 2
            - List item 3...
            - Lis...
            - Zzz
        """).strip()
        res = block_to_block_type(text)
        self.assertEqual(res, BlockType.UNORDERED_LIST)

    def test_blocktype_ordered_list(self):
        text = textwrap.dedent("""
            1. List item 1
            2. List item 2
            3. List item 3...
            4. Lis...
            5. Zzz
            6. zzzz
            7. zzzzz
            8. zzzzzz
            9. zzzzzzz
            10. zzzzzzzz
        """).strip()
        res = block_to_block_type(text)
        self.assertEqual(res, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = textwrap.dedent("""
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = textwrap.dedent("""
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """).strip()

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_with_inline(self):
        md = "## Hello **world**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Hello <b>world</b></h2></div>")

    def test_unordered_list_with_inline(self):
        md = "- item one\n- item **two**\n- item three"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item <b>two</b></li><li>item three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )

    def test_blockquote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")
