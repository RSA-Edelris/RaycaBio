
import base64, urllib.request, urllib.error, os, json as _json

FILE = OUT  # /home/ubuntu/rayca-sessions/.../HTE_screen_chat_log.pdf
REPO = "RSA-Edelris/RaycaBio"
DEST = "studies/a26cc075-95a4-4e76-8438-9c117af1a9de/chat_logs/HTE_screen_chat_log.pdf"

# Read GitHub token from environment
token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
print("Token found:", bool(token))

# base64 encode the PDF
with open(FILE, "rb") as fh:
    b64 = base64.b64encode(fh.read()).decode()

url = f"https://api.github.com/repos/{REPO}/contents/{DEST}"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json",
}

# Check if file already exists (get SHA)
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as r:
        existing = _json.loads(r.read())
        sha = existing.get("sha", "")
except urllib.error.HTTPError as e:
    sha = "" if e.code == 404 else (_ for _ in ()).throw(e)

payload = {"message": "docs: add HTE screen chat log PDF", "content": b64}
if sha:
    payload["sha"] = sha

data = _json.dumps(payload).encode()
req2 = urllib.request.Request(url, data=data, headers=headers, method="PUT")
with urllib.request.urlopen(req2) as r:
    resp = _json.loads(r.read())

commit_url = resp.get("commit", {}).get("html_url", "")
print("Pushed:", commit_url)
