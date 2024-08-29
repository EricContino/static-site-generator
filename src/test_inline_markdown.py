import unittest

from textnode import *
from inline_markdown import *


class TestInlineMarkdown(unittest.TestCase):
    def test_inline_markdown(self):
        n1 = TextNode("*The start* of this node will be delimited", text_type_text)
        n2 = TextNode("The middle of *this node* will be delimited", text_type_text)
        n3 = TextNode("The end of this node will *be delimited*", text_type_text)
        actual = split_nodes_delimiter([n1,n2,n3],delimiter_italic, text_type_italic)

        e1 = TextNode("The start", text_type_italic)
        e2 = TextNode(" of this node will be delimited",text_type_text)
        e3 = TextNode("The middle of ",text_type_text)
        e4 = TextNode("this node",text_type_italic)
        e5 = TextNode(" will be delimited",text_type_text)
        e6 = TextNode("The end of this node will ",text_type_text)
        e7 = TextNode("be delimited",text_type_italic)
        expected = [e1,e2,e3,e4,e5,e6,e7]
        self.assertEqual(expected, actual)

    def test_inline_markdown_non_text(self):
        n1 = TextNode("*The start* of this node will be delimited", text_type_italic)
        actual = split_nodes_delimiter([n1],delimiter_italic, text_type_italic)
        self.assertEqual([n1],actual)

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(actual, expected)

    def test_extract_images_given_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_images(text)
        self.assertEqual(actual, [])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(actual, expected)

    def test_extract_links_given_imgs(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_links(text)
        self.assertEqual(actual, [])
    

if __name__ == "__main__":
    unittest.main()