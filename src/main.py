from textnode import TextNode, TextType


def main():
    text_node = TextNode("hello world", TextType.BOLD, "abc.com")
    print(text_node)


main()
