
import os, base64, subprocess, json

# Get token from git credential store or env
token = os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GH_TOKEN", "")

# Try to extract from git config credential helper
if not token:
    result = subprocess.run(["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("password="):
            token = line.split("=", 1)[1].strip()
            break

print("Token found:", bool(token), "length:", len(token) if token else 0)
print("Env vars with TOKEN:", [k for k in os.environ if "TOKEN" in k or "GH_" in k or "GITHUB" in k])
