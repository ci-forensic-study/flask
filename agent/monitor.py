import os
import time
import json
import hashlib

def repo_fingerprint(path="."):
    h = hashlib.sha256()
    for root, _, files in os.walk(path):
        for f in files:
            if ".git" in root or "__pycache__" in root:
                continue
            try:
                with open(os.path.join(root, f), "rb") as file:
                    h.update(file.read())
            except:
                pass
    return h.hexdigest()

log_entry = {
    "timestamp": time.time(),
    "commit": os.getenv("GITHUB_SHA"),
    "file_count": sum(len(files) for _, _, files in os.walk(".")),
    "repo_fingerprint": repo_fingerprint()
}

log_file = "forensic_log.jsonl"

with open(log_file, "a") as f:
    f.write(json.dumps(log_entry) + "\n")

print("Forensic log entry recorded:")
print(json.dumps(log_entry, indent=2))
