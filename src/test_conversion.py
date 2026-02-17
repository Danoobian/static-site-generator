import unittest

from conversion import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)
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
            TextNode("**abc**", TextType.BOLD),
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

    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_results = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(extract_markdown_images(text), expected_results)

    def test_one_image_extraction(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_none_image_extraction(self):
        text = "This text contains no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_nested_image_extraction(self):
        text = "This is text with a ![rick[ roll]](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com(/fJRm4Vk.jpeg))"
        self.assertEqual(extract_markdown_images(text), [])

    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_results = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(extract_markdown_links(text), expected_results)

    def test_one_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected_results = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected_results)

    def test_none_link_extraction(self):
        text = "This text contains no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_image_link_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_nested_link_extraction(self):
        text = "This is text with a link [to boot[ dev]](https://www.boot.dev) and [to youtube](https://www.youtube.com/(@bootdotdev))"
        self.assertEqual(extract_markdown_links(text), [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode(
            "This is text without an image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without an image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_only_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_no_links(self):
        node = TextNode(
            "This is text without a link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("This is text without a link", TextType.TEXT)],
            new_nodes,
        )

    def test_split_only_links(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
