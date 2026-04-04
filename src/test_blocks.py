import unittest
from block import markdown_to_blocks, block_to_block_type, BlockType

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_type(self):
        block = "This is paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_block_to_type_un_list(self):
        block = "- This is a list\n- with items"
        self.assertEqual(BlockType.UN_LIST, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()