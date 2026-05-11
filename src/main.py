import sys

from src.generatepage import generate_pages_recursive
from src.textnode import TextNode, TextType
from src.copydir import copy_dir_contents


def main():
    basepath = sys.argv[0] or '/'
    print(basepath)

    copy_dir_contents("./static", "./docs")
    generate_pages_recursive('content', 'template.html', 'docs', basepath)


main()
