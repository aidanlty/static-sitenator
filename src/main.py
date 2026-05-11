from src.generatepage import generate_pages_recursive
from src.textnode import TextNode, TextType
from src.copydir import copy_dir_contents


def main():
    text_node = TextNode("hello world", TextType.BOLD, "abc.com")
    print(text_node)

    copy_dir_contents("./static", "./public")
    generate_pages_recursive('content', 'template.html', 'public')


main()
