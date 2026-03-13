def markdown_to_blocks(markdown):
    
    initial_blocks = markdown.split('\n\n')
    new_blocks = []
    
    for block in initial_blocks:
        if block.strip() != '':
            new_blocks.append(block.strip())

    return new_blocks