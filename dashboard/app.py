import json
import sys
from pathlib import Path

from flask import Flask, render_template, redirect


# ---------------------------------------------------------
# PATH CONFIGURATION
# ---------------------------------------------------------

# p078-engine/
# ├── main.py
# ├── audit_log.json
# └── dashboard/
#     ├── app.py
#     └── templates/
#         └── index.html

BASE_DIR = Path(__file__).resolve().parent.parent

# Make the project root available for imports like:
# from main import main
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ---------------------------------------------------------
# FLASK APP
# ---------------------------------------------------------

app = Flask(__name__)

AUDIT_FILE = BASE_DIR / "audit_log.json"


# ---------------------------------------------------------
# LOAD AUDIT DATA
# ---------------------------------------------------------

def load_audit():
    try:
        with open(AUDIT_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ---------------------------------------------------------
# REFRESH FROM AZURE
# ---------------------------------------------------------

@app.route("/refresh")
def refresh():
    """
    Refresh the dashboard using the current Azure
    Guest Configuration state.

    IMPORTANT:
    This performs evaluation only.
    It does NOT execute VM remediation.
    """

    from main import main as run_enforcement

    run_enforcement()

    return redirect("/")


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

@app.route("/")
def dashboard():

    audit = load_audit()

    summary = audit.get("summary", {})

    findings = audit.get("findings", [])

    remediation_history = audit.get(
        "remediation_history",
        []
    )

    compliant = summary.get(
        "compliant",
        0
    )

    safe = summary.get(
        "safe",
        0
    )

    exception = summary.get(
        "exception",
        0
    )

    review = summary.get(
        "review",
        0
    )

    manual = summary.get(
        "manual",
        0
    )

    total = (
        compliant
        + safe
        + exception
        + review
        + manual
    )

    if total:
        compliance_percentage = round(
            (compliant / total) * 100,
            1
        )
    else:
        compliance_percentage = 0

    return render_template(
        "index.html",

        audit=audit,

        summary=summary,

        findings=findings,

        remediation_history=remediation_history,

        total=total,

        compliance_percentage=compliance_percentage,
    )


# ---------------------------------------------------------
# START SERVER
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
