import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
    def test_props_to_html(self):
        test_dict = {
                        "href": "https://www.google.com",
                        "target": "_blank",
                    }
        node = HTMLNode("a", None, None, test_dict)
        check_string =  ' href="https://www.google.com" target="_blank" '
        self.assertEqual(node.props_to_html(), check_string)
    
    def test_value_eq(self):
        node = HTMLNode("p", "PING", None, None)
        node2 = HTMLNode("p", "PING", None, None)
        self.assertEqual(node.value, node2.value)

    def test_repr(self):
        check_string = "HTMLNode(p, PING, None, None)"
        node = HTMLNode("p", "PING", None, None)
        self.assertEqual(repr(node), check_string)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

if __name__ == "__main__":
    unittest.main()