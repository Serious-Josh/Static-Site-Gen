import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()