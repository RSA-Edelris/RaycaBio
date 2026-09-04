
from modulon.governance.toolkit import aidd_tool_schema
import json

for tool_id in ['easy-md', 'dynamate']:
    schema = aidd_tool_schema(tool_id)
    print(f"\n{'='*60}")
    print(f"TOOL: {tool_id}")
    print(f"{'='*60}")
    # Print inputs and key fields only
    print("Required:", schema.get('required'))
    print("Inputs:")
    for k, v in schema.get('inputs', {}).items():
        desc = v.get('description', '')[:120]
        print(f"  {k} [{v.get('type')}] req={v.get('required',False)}: {desc}")
