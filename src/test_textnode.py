import unittest

from textnode import *
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_diff_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is not a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_diff_url_default_url(self):
        node = TextNode("This is not a text node", "bold", "www.google.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_diff_urls(self):
        node = TextNode("This is not a text node", "bold", "www.google.com")
        node2 = TextNode("This is a text node", "bold", "www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        expected = "TextNode(This is not a text node, bold, www.google.com)"
        node = TextNode("This is not a text node", "bold", "www.google.com")
        self.assertEqual(f"{node}", expected)

    def test_repr_default_url(self):
        expected = "TextNode(This is not a text node, bold, None)"
        node = TextNode("This is not a text node", "bold")
        self.assertEqual(f"{node}", expected)

    def test_convert_text_node_text(self):
        tn = TextNode("test", "text")
        expected = LeafNode(None, "test")
        actual = text_node_to_html_node(tn)
        self.assertEqual(expected, actual)

    def test_convert_text_node_bold(self):
        tn = TextNode("test", "bold")
        expected = LeafNode("b", "test")
        actual = text_node_to_html_node(tn)
        self.assertEqual(expected, actual)

    def test_convert_text_node_italic(self):
        tn = TextNode("test", "italic")
        expected = LeafNode("i", "test")
        actual = text_node_to_html_node(tn)
        self.assertEqual(expected, actual)

    def test_convert_text_node_code(self):
        tn = TextNode("test", "code")
        expected = LeafNode("code", "test")
        actual = text_node_to_html_node(tn)
        self.assertEqual(expected, actual)

    def test_convert_text_node_link(self):
        tn = TextNode("test", "link", "www.google.com")
        props = { "href":"www.google.com"}
        expected = LeafNode("a", "test", props)
        actual = text_node_to_html_node(tn)
        self.assertEqual(expected, actual)

    def test_convert_text_node_image(self):
        tn = TextNode("test", "image", "www.google.com")
        props = {
            "src":"www.google.com",
            "alt":"test"
        }
        expected = LeafNode("img", "",props)
        actual = text_node_to_html_node(tn)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()