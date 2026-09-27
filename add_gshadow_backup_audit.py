import json
from pathlib import Path


AUDIT_FILE = Path("audit_log.json")

RULE = "Ensure file permissions on /etc/gshadow- are configured"


def main():
    print("\n=== P078 AUDIT MIGRATION ===\n")

    if not AUDIT_FILE.exists():
        print("ERROR: audit_log.json not found.")
        return

    with open(AUDIT_FILE, "r") as file:
        audit_log = json.load(file)

    history = audit_log.setdefault("remediation_history", [])

    # Prevent duplicate historical entry
    already_exists = any(
        entry.get("rule") == RULE
        and entry.get("action") == "REMEDIATED"
        and entry.get("before") == "640"
        and entry.get("after") == "400"
        for entry in history
    )

    if already_exists:
        print("Audit entry already exists.")
        print("No duplicate entry created.")
        return

    # This records the remediation that already happened.
    # Exact execution timestamp is intentionally unknown.
    entry = {
        "timestamp": None,
        "vm": "vm-p078-demo",
        "assignment": "AzureLinuxBaseline",
        "rule": RULE,
        "decision": "SAFE",
        "action": "REMEDIATED",
        "command": "chmod 400 /etc/gshadow-",
        "before": "640",
        "after": "400",
        "verification": "PASSED",
        "source": "historical_remediation_record"
    }

    history.append(entry)

    with open(AUDIT_FILE, "w") as file:
        json.dump(audit_log, file, indent=2)

    print("Audit entry added successfully.")
    print()
    print("Rule         :", RULE)
    print("Decision     : SAFE")
    print("Action       : REMEDIATED")
    print("Command      : chmod 400 /etc/gshadow-")
    print("Before       : 640")
    print("After        : 400")
    print("Verification : PASSED")
    print("Source       : Historical remediation record")
    print()
    print("audit_log.json updated.")


if __name__ == "__main__":
    main()
