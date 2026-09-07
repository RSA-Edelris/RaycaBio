
# Read the raw SDF text and extract properties manually
import re

# Show first pose block to understand the format
blocks = sdf_text.split("$$$$")
print(f"Total blocks: {len(blocks)}")
print("\n=== POSE 1 BLOCK (last 800 chars) ===")
print(blocks[0][-800:])
