import sys

from src.generatepage import generate_pages_recursive
from src.textnode import TextNode, TextType
from src.copydir import copy_dir_contents


def main():
    basepath = '/'
    if len(sys.argv) >= 2:
        basepath = sys.argv[1] or '/'  # basepath : static-sitenator
    print(basepath)

    copy_dir_contents("./static", "./docs")
    generate_pages_recursive('content', 'template.html', 'docs', basepath)


main()
