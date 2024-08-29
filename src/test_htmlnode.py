import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    #========================================
    # HTMLNode
    #========================================
    def test_props_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        node = HTMLNode(None,None,None,props)
        self.assertEqual(expected, node.props_to_html())

    def test_repr(self):
        tag = "p"
        value = "Plain text"
        child = HTMLNode()
        children = [child]
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = HTMLNode(tag, value, children, props)
        expected = f"HTMLNode({tag}, {value}, children: {children}, {props})"
        self.assertEqual(expected, f"{node}")

    def test_repr_default_vals(self):
        node = HTMLNode()
        expected = f"HTMLNode(None, None, children: None, None)"
        self.assertEqual(expected, f"{node}")

    #========================================
    # LeafNode
    #========================================
    def test_to_html(self):
        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
        }
        node = LeafNode("p", "text", props)
        expected = "<p href=\"https://www.google.com\" target=\"_blank\">text</p>"
        self.assertEqual(expected, node.to_html())

    def test_to_html_no_tag(self):
        node = LeafNode(None,"test")
        self.assertEqual("test", node.to_html())

    #========================================
    # ParentNode
    #========================================
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )



if __name__ == "__main__":
    unittest.main()