import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_markdown_to_blocks_oneline(self):
        markdown = "This is a **block**"
        self.assertEqual(markdown_to_blocks(markdown), [markdown])

    def test_markdown_to_blocks_normal(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        block = "### HEADING"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_wrong_heading(self):
        block = "######### HEADING"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = """```python
print("text")
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_wrong_code(self):
        block = "```print('text')```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = """> line1
>line2
> line3"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_wrong_quote(self):
        block = """> line1
line2
> line3
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_indent_quote(self):
        block = """> line1
 > line2
  > line3
"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = """- element1
 - element2
  - element3"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_wrong_unordered_list(self):
        block = """- element1
 element2
  - element3"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_space_unordered_list(self):
        block = """- element1
-element2
- element3"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = """1. first
 2. second
  3. third"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_0start_ordered_list(self):
        block = """0. first
 2. second
  3. third"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_ordered_list(self):
        block = """1.first
 2. second
  3.third"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_missing_ordered_list(self):
        block = """1.first
second
  3.third"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        block = "test string"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
