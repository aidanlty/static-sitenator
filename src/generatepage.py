from genericpath import isfile
import os
from tempfile import template

from src.formatter.block_formatter import markdown_to_html_node


def extract_title(md):
    lines = md.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    else:
        raise Exception("Error: No h1 header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}...")
    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        tp = f.read()

    title = extract_title(md)
    html_nodes = markdown_to_html_node(md)
    html_string = html_nodes.to_html()
    
    tp = tp.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    tp = tp.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(tp)
    print(f'Generated    : ./{dest_path}')

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    nested_items = os.listdir(dir_path_content)
    for item in nested_items:
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(from_path):
            dest_path = dest_path.replace('.md', '.html')
            generate_page(from_path, template_path, dest_path, basepath)
        if os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
            