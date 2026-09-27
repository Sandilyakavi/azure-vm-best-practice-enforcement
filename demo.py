import json
from pathlib import Path

from main import main as run_enforcement


AUDIT_FILE = Path("audit_log.json")


def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def show_final_state():
    if not AUDIT_FILE.exists():
        print("\nAudit file not found.")
        return

    with open(AUDIT_FILE, "r") as file:
        audit = json.load(file)

    summary = audit.get("summary", {})

    print_section("P078 FINAL DEMO STATE")

    print(f"VM          : {audit.get('vm', 'Unknown')}")
    print(f"Assignment  : {audit.get('assignment', 'Unknown')}")
    print()

    print(f"Compliant   : {summary.get('compliant', 0)}")
    print(f"Safe        : {summary.get('safe', 0)}")
    print(f"Exception   : {summary.get('exception', 0)}")
    print(f"Review      : {summary.get('review', 0)}")
    print(f"Manual      : {summary.get('manual', 0)}")
    print(f"Approved    : {summary.get('approved', 0)}")
    print(f"Blocked     : {summary.get('blocked', 0)}")

    remediation_history = audit.get("remediation_history", [])

    print()
    print(f"Remediation records : {len(remediation_history)}")

    for item in remediation_history:
        print(
            f"  - {item.get('rule', 'Unknown')} : "
            f"{item.get('before', '-')} -> "
            f"{item.get('after', '-')} : "
            f"{item.get('verification', 'UNKNOWN')}"
        )


def main():
    print()
    print("=" * 60)
    print("       P078 AZURE VM ENFORCEMENT DEMO")
    print("=" * 60)

    print()
    print("Mode        : EVALUATION / DRY-RUN")
    print("VM Changes  : DISABLED")
    print("Audit       : ENABLED")

    print_section("RUNNING ENFORCEMENT WORKFLOW")

    print("1. Collecting Guest Configuration findings...")
    print("2. Evaluating best-practice rules...")
    print("3. Checking exceptions...")
    print("4. Checking approvals...")
    print("5. Classifying remediation decisions...")
    print("6. Updating audit state...")
    print()

    run_enforcement()

    show_final_state()

    print_section("P078 DEMO COMPLETE")

    print("VM changes performed : NO")
    print("Audit log updated    : YES")
    print("Dashboard available  : http://127.0.0.1:5000")

    print()
    print("Workflow:")
    print(
        "Detect -> Evaluate -> Exception Check -> "
        "Approval Check -> Decision -> Audit"
    )

    print()


if __name__ == "__main__":
    main()
