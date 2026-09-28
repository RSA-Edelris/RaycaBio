
import re, subprocess, os, shutil, tempfile

CRED_FILE = "/home/ubuntu/.credentials/GitHub/GitHub-Fine-Grained-PAT-Tpken_ClaudeCode_RaycaPlatformDevelopment.txt"
with open(CRED_FILE) as f:
    content = f.read()

m = re.search(r'Token="([^"]+)"', content)
token = m.group(1).strip() if m else ""
print("Token extracted:", bool(token), "| Length:", len(token), "| Prefix:", token[:12])

# Try the API directly with the proper token
import urllib.request, base64, json as _json

REPO = "RSA-Edelris/RaycaBio"
DEST = "studies/a26cc075-95a4-4e76-8438-9c117af1a9de/chat_logs/HTE_screen_chat_log.pdf"
PDF_PATH = "/home/ubuntu/rayca-sessions/a26cc075-95a4-4e76-8438-9c117af1a9de-26995afd3529/HTE_screen_chat_log.pdf"

with open(PDF_PATH, "rb") as fh:
    b64 = base64.b64encode(fh.read()).decode()

url = f"https://api.github.com/repos/{REPO}/contents/{DEST}"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
}

# Check if exists
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as r:
        sha = _json.loads(r.read()).get("sha", "")
except urllib.error.HTTPError as e:
    sha = "" if e.code == 404 else None
    if sha is None:
        print(f"Error checking existence: {e.code} {e.reason}")

payload = {"message": "docs: add HTE screen chat log PDF (929EDL2056)", "content": b64,
           "committer": {"name": "Rayca Platform Development", "email": "platform@rayca.ai"}}
if sha:
    payload["sha"] = sha

data = _json.dumps(payload).encode()
req2 = urllib.request.Request(url, data=data, headers=headers, method="PUT")
try:
    with urllib.request.urlopen(req2) as r:
        resp = _json.loads(r.read())
        print("Pushed:", resp.get("commit", {}).get("html_url", ""))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"Push error {e.code}: {body[:200]}")
