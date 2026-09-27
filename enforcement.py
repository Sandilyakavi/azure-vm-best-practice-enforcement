import json

from rule_engine import evaluate_findings
from approval_manager import is_approved


DRY_RUN = True


REMEDIATION_COMMANDS = {
    "Ensure file permissions on /etc/gshadow are configured":
        "chmod 400 /etc/gshadow",

    "Ensure file permissions on /etc/gshadow- are configured":
        "chmod 400 /etc/gshadow-",

    "Ensure file permissions on /etc/shadow are configured":
        "chmod 400 /etc/shadow",

    "Ensure file permissions on /etc/shadow- are configured":
        "chmod 400 /etc/shadow-",

    "Ensure logger configuration files are restricted":
        "chmod 640 /etc/rsyslog.conf",

    "Ensure permissions on /etc/cron.d are configured":
        "chmod 700 /etc/cron.d",

    "Ensure permissions on /etc/cron.daily are configured":
        "chmod 700 /etc/cron.daily",

    "Ensure permissions on /etc/ssh/sshd_config are configured":
        "chmod 600 /etc/ssh/sshd_config"
}


def get_base_rule(resource):
    if " (CIS:" in resource:
        return resource.split(" (CIS:")[0].strip()

    return resource.strip()


def build_execution_plan(results):

    plan = []

    for result in results:

        if result["decision"] != "SAFE":
            continue

        rule = get_base_rule(result["resource"])

        if not is_approved(rule):
            continue

        command = REMEDIATION_COMMANDS.get(rule)

        if command is None:
            continue

        plan.append({
            "rule": rule,
            "resource": result["resource"],
            "command": command,
            "status": result["status"],
            "reason": result["reason"]
        })

    return plan


def main():

    print("\n==========================================")
    print("       P078 ENFORCEMENT ENGINE")
    print("==========================================\n")

    print("MODE :", "DRY RUN" if DRY_RUN else "EXECUTION")
    print("VM changes :", "DISABLED" if DRY_RUN else "ENABLED")

    print("\nSTEP 1: Collecting current findings...\n")

    results = evaluate_findings()

    print("\nSTEP 2: Building approved remediation plan...\n")

    plan = build_execution_plan(results)

    print(f"Approved remediation candidates : {len(plan)}")

    if not plan:
        print("\nNo approved remediation candidates.")
        print("No VM changes performed.")
        return

    print("\n=== APPROVED REMEDIATION PLAN ===\n")

    for index, item in enumerate(plan, start=1):

        print(f"{index}. {item['rule']}")
        print(f"   Command : {item['command']}")
        print(f"   Status  : {item['status']}")
        print()

    if DRY_RUN:

        print("==========================================")
        print("             DRY RUN RESULT")
        print("==========================================")

        print(f"Candidates : {len(plan)}")
        print("Executed   : 0")
        print("VM changed : NO")

        return

    print("\nExecution mode enabled.")
    print("Remediation execution is intentionally separated.")
    print("Use remediation.py only after explicit approval.")


if __name__ == "__main__":
    main()
