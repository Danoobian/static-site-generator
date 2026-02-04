import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a link", TextType.LINK)
        node2 = TextNode("This is a link", TextType.LINK, url="https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_same(self):
        node = TextNode("This is a link", TextType.LINK, url="https://www.boot.dev")
        node2 = TextNode("This is a link", TextType.LINK, url="https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url_missing(self):
        node = TextNode("This is a link", TextType.LINK)
        node2 = TextNode("This is a link", TextType.LINK, url=None)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
