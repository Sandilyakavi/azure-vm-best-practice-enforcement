import json
from datetime import datetime, timezone

from rule_engine import evaluate_findings


AUDIT_FILE = "audit_log.json"


def write_audit(results):

    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "vm": "vm-p078-demo",
        "assignment": "AzureLinuxBaseline",
        "summary": {
            "compliant": 0,
            "safe": 0,
            "exception": 0,
            "review": 0,
            "manual": 0
        },
        "findings": results
    }

    # Count decisions
    for result in results:

        decision = result["decision"].lower()

        if decision == "compliant":
            audit_entry["summary"]["compliant"] += 1

        elif decision == "safe":
            audit_entry["summary"]["safe"] += 1

        elif decision == "exception":
            audit_entry["summary"]["exception"] += 1

        elif decision == "review":
            audit_entry["summary"]["review"] += 1

        elif decision == "manual":
            audit_entry["summary"]["manual"] += 1

    # Write audit file
    with open(AUDIT_FILE, "w") as file:
        json.dump(audit_entry, file, indent=2)

    print(f"\nAudit log written to: {AUDIT_FILE}")


def main():

    print("\n=== P078 AUDIT ENGINE ===\n")

    # Run collector + rule engine
    results = evaluate_findings()

    # Generate audit log
    write_audit(results)

    # Calculate summary
    summary = {
        "compliant": 0,
        "safe": 0,
        "exception": 0,
        "review": 0,
        "manual": 0
    }

    for result in results:

        decision = result["decision"].lower()

        if decision in summary:
            summary[decision] += 1

    print("\n=== P078 AUDIT SUMMARY ===\n")

    print(
        json.dumps(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "vm": "vm-p078-demo",
                "assignment": "AzureLinuxBaseline",
                "summary": summary
            },
            indent=2
        )
    )


if __name__ == "__main__":
    main()
