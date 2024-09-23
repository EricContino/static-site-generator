import os
import shutil

from copystatic import *
from markdown_blocks import markdown_to_html_node
from htmlnode import *


dir_path_static = "./static"
dir_path_public = "./public"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page("./content/index.md", "./template.html", "./public/index.html")

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line[4:]
            return title.strip()
    raise ValueError("Invalid markdown, no title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = os.open(from_path)
    markdown = from_file.read()
    os.close(from_file)
    template_file = os.open(template_path)
    template = template_file.read()
    os.close(template_file)

    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_node.to_html())

    dest_file = os.open(dest_path, "w")
    dest_file.write(html)
    dest_file.close()


main()
