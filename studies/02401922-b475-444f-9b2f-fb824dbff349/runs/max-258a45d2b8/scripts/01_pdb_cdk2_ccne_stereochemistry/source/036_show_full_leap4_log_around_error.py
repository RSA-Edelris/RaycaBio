
# Show full leap4 log around the error
with open('leap.log') as f:
    lines = f.readlines()
# Find error context
for i, l in enumerate(lines):
    if 'FATAL' in l or 'cannot add bond' in l:
        start = max(0, i-10)
        for ll in lines[start:i+5]:
            print(ll, end='')
        print('---')
