
# Show leap.log errors
with open('leap.log') as f:
    log = f.read()

# Print error-relevant lines
for l in log.split('\n'):
    if any(k in l for k in ['ERROR','FATAL','error','Unable','unknown','Unknown','Warning']):
        print(l)
