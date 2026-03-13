from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "c"
    QUOTE = "q"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def block_to_block_type(block):

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    elif all(item.startswith("- ") for item in lines):
        return BlockType.UNORDERED_LIST

    elif block.startswith('1. '):
        if all(line.startswith(f'{i+1}. ') for i, line in enumerate(lines)):
            return BlockType.ORDERED_LIST
     
    return BlockType.PARAGRAPH