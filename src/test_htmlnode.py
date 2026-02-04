import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        test_tag = "p"
        test_val = "this is a pragraph"
        node = HTMLNode(test_tag, test_val)
        self.assertTrue(str(node) is not None)
        self.assertTrue(str(node) != "")
        self.assertEqual(node.tag, test_tag)
        self.assertEqual(node.value, test_val)

    def test_emptyval_leafnode(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_emptytag_leafnode(self):
        test_val = "test text here"
        node = LeafNode(None, test_val)
        self.assertEqual(node.to_html(), test_val)

    def test_to_html_leafnode(self):
        test_tag = "a"
        test_val = "Boot.dev"
        test_props = {"href": "https://www.boot.dev"}
        node = LeafNode(test_tag, test_val, test_props)
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Boot.dev</a>')

    def test_emptyprops_leafnode(self):
        test_tag = "p"
        test_val = "this is a pragraph"
        test_props = None
        node = LeafNode(test_tag, test_val, test_props)
        self.assertEqual(node.to_html(), f"<{test_tag}>{test_val}</{test_tag}>")

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

    def test_notag_parentnode(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "parent node must have tag"):
            parent_node.to_html()

    def test_nochildren_parentnode(self):
        parent_node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError, "parent node must have children"):
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()
