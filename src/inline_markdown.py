import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            sections = node.text.split(delimiter)
            split_nodes = []
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            for i in range(0, len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i],text_type_text))
                else:
                    split_nodes.append(TextNode(sections[i],text_type))
            new_nodes.extend(split_nodes)                  
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    return split_nodes_with_url(old_nodes, extract_markdown_images, text_type_image, recreate_img_markdown)

def split_nodes_link(old_nodes):
    return split_nodes_with_url(old_nodes, extract_markdown_links, text_type_link, recreate_link_markdown)

def recreate_img_markdown(text, url):
    return f"![{text}]({url})"

def recreate_link_markdown(text, url):
    return f"[{text}]({url})"

def split_nodes_with_url(old_nodes, extract_markdown, text_type, markdown_recreator):
    new_nodes = []
    for node in old_nodes:
        split_nodes = []
        if node.text_type == text_type_text:
            extracted = extract_markdown(node.text)
            if len(extracted) == 0:
                new_nodes.append(node)
            else:
                sections = node.text.split(markdown_recreator(extracted[0][0],extracted[0][1]))
                
                if sections[0] == "":
                    split_nodes.append(TextNode(extracted[0][0],text_type, extracted[0][1]))
                    next_level_nodes = split_nodes_with_url([TextNode(sections[1],text_type_text)], extract_markdown, text_type, markdown_recreator)
                    split_nodes.extend(next_level_nodes)
                elif sections[1] == "":
                    split_nodes.append(TextNode(sections[0], text_type_text))
                    split_nodes.append(TextNode(extracted[0][0],text_type, extracted[0][1]))
                else:
                    split_nodes.append(TextNode(sections[0], text_type_text))
                    split_nodes.append(TextNode(extracted[0][0],text_type, extracted[0][1]))
                    next_level_nodes = split_nodes_with_url([TextNode(sections[1],text_type_text)], extract_markdown, text_type, markdown_recreator)
                    split_nodes.extend(next_level_nodes)
        else:
            new_nodes.append(node)
        new_nodes.extend(split_nodes)
    return new_nodes
                
def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    bolds = split_nodes_delimiter([node], delimiter_bold, text_type_bold)
    italics = split_nodes_delimiter(bolds, delimiter_italic, text_type_italic)
    codes = split_nodes_delimiter(italics, delimiter_code, text_type_code)
    imgs = split_nodes_image(codes)
    links = split_nodes_link(imgs)
    return links
