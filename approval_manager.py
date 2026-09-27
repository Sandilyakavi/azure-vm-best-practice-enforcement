import json

APPROVAL_FILE = "approvals.json"


def load_approvals():
    try:
        with open(APPROVAL_FILE, "r") as file:
            data = json.load(file)

        return set(data.get("approved_rules", []))

    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def is_approved(rule):
    approved_rules = load_approvals()

    return rule in approved_rules


def get_approval_status(rule):
    if is_approved(rule):
        return "APPROVED"

    return "NOT_APPROVED"


if __name__ == "__main__":

    print("\n=== P078 APPROVAL MANAGER ===\n")

    test_rule = "Ensure file permissions on /etc/gshadow are configured"

    status = get_approval_status(test_rule)

    print(f"Rule   : {test_rule}")
    print(f"Status : {status}")

    print("\nNo VM changes performed.")
