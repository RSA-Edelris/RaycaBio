
# Check what built-in functions are available in this namespace
import builtins
provided = [n for n in dir(builtins) if not n.startswith('_')]
print("builtins:", provided[:20])

# Check the special provided functions
special = ['dispatch', 'doing', 'blocked', 'finish', 'found', 'deciding', 
           'rayca_toolkit', 'rayca_tools', 'mcp_servers']
for s in special:
    try:
        v = eval(s)
        print(f"{s}: {type(v).__name__}")
    except: 
        print(f"{s}: not found")

# Check rayca_toolkit for any cleanup/admin functions
if 'rayca_toolkit' in dir():
    print("\nrayca_toolkit methods:", [m for m in dir(rayca_toolkit) if not m.startswith('_')])
