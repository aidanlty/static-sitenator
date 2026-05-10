from textnode import TextNode, TextType
from copydir import copy_dir_contents


def main():
    text_node = TextNode("hello world", TextType.BOLD, "abc.com")
    print(text_node)
    
    copy_dir_contents('./static', './public')


main()
