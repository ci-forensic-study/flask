import os
import time
import json
import hashlib

WORKFLOW_PATH = ".github/workflows/ci.yml"
REQUIREMENTS_PATH = "requirements.txt"

# -------------------------
# Utility: hash a single file
# -------------------------
def file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

# -------------------------
# Utility: hash entire repo
# -------------------------
def repo_fingerprint(path="."):
    h = hashlib.sha256()
    for root, _, files in os.walk(path):
        for f in files:
            if ".git" in root or "__pycache__" in root:
                continue
            try:
                file_path = os.path.join(root, f)
                with open(file_path, "rb") as file:
                    h.update(file.read())
            except Exception:
                pass
    return h.hexdigest()

# -------------------------
# Count files in repo
# -------------------------
def count_files(path="."):
    count = 0
    for root, _, files in os.walk(path):
        if ".git" in root or "__pycache__" in root:
            continue
        count += len(files)
    return count

# -------------------------
# Count workflow steps
# -------------------------
def count_workflow_steps(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
        # Count lines that define a step using "- name:"
        step_count = sum(1 for line in lines if line.strip().startswith("- name:"))
        return step_count
    except Exception:
        return None

# -------------------------
# Collect forensic data
# -------------------------
workflow_hash = file_hash(WORKFLOW_PATH)
requirements_hash = file_hash(REQUIREMENTS_PATH)
workflow_step_count = count_workflow_steps(WORKFLOW_PATH)

log_entry = {
    "timestamp": time.time(),
    "commit": os.getenv("GITHUB_SHA"),
    "file_count": count_files(),
    "repo_fingerprint": repo_fingerprint(),
    "workflow_hash": workflow_hash,
    "requirements_hash": requirements_hash,
    "workflow_step_count": workflow_step_count
}

log_file = "forensic_log.jsonl"

with open(log_file, "a") as f:
    f.write(json.dumps(log_entry) + "\n")

print("Forensic log entry recorded:")
print(json.dumps(log_entry, indent=2))
