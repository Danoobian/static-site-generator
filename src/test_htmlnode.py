import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_processing(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        expected_props = ' href="https://www.google.com" target="_blank"'
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), expected_props)

    def test_none_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_init(self):
        node = HTMLNode("p", "this is a pragraph")
        self.assertTrue(str(node) is not None)
        self.assertTrue(str(node) != "")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "this is a pragraph")


if __name__ == "__main__":
    unittest.main()
