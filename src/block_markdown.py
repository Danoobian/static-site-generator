def markdown_to_blocks(markdown):
    """
    Convert markdown sting into a list of non-empty, stripped block of strings.
    """
    markdown_blocks = markdown.split("\n\n")
    return [
        markdown_block.strip()
        for markdown_block in markdown_blocks
        if markdown_block.strip()
    ]
