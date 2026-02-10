import unittest

from conversion import split_nodes_delimiter, text_node_to_html_node
from textnode import TextNode, TextType


class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image"}
        )

    def test_unbalanced_delimiter(self):
        node = TextNode("abc `def ghi", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_one_pair_delimiter(self):
        node = TextNode("abc `def` ghi", TextType.TEXT)
        expected_nodes = [
            TextNode("abc ", TextType.TEXT),
            TextNode("def", TextType.CODE),
            TextNode(" ghi", TextType.TEXT),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), expected_nodes
        )

    def test_two_pair_delimiter(self):
        node = TextNode("`abc` def `ghi`", TextType.TEXT)
        expected_nodes = [
            TextNode("abc", TextType.CODE),
            TextNode(" def ", TextType.TEXT),
            TextNode("ghi", TextType.CODE),
        ]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), expected_nodes
        )

    def test_zero_delimiter(self):
        node = TextNode("abc def ghi", TextType.TEXT)
        expected_nodes = [TextNode("abc def ghi", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE), expected_nodes
        )

    def test_multiple_mixed_delimiter(self):
        nodes = [
            TextNode("*abc*", TextType.BOLD),
            TextNode("hello `world`", TextType.TEXT),
            TextNode("_xyz_", TextType.ITALIC),
        ]
        expected_nodes = [
            TextNode("**abc**", TextType.BOLD),
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.CODE),
            TextNode("_xyz_", TextType.ITALIC),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE), expected_nodes
        )


if __name__ == "__main__":
    unittest.main()
