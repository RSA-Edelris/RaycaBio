
# Check episodic memory for known protacfold issues
r = memory.episodic(query="protacfold DataLoader worker crash prediction failure", k=10)
for m in r:
    print(m.get('subject',''), '|', m.get('body','')[:300])
    print()
