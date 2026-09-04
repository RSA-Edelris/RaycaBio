
from modulon.governance.toolkit import aidd_tool_schema
schema = aidd_tool_schema('gromacs')
import json
print(json.dumps(schema, indent=2))
