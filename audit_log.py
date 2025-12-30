import json
from datetime import datetime

def log_event(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()
    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")
