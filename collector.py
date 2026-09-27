from azure.identity import AzureCliCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest


SUBSCRIPTION_ID = "0f5fd928-8b42-4378-b96c-576495b41522"
VM_NAME = "vm-p078-demo"
ASSIGNMENT_NAME = "AzureLinuxBaseline"


def collect_baseline_findings():
    credential = AzureCliCredential()
    client = ResourceGraphClient(credential)

    query = f"""
    guestconfigurationresources
    | where type =~ 'microsoft.guestconfiguration/guestconfigurationassignments'
    | where name =~ '{ASSIGNMENT_NAME}'
    | where properties.targetResourceId has '{VM_NAME}'
    | extend report = properties.latestAssignmentReport
    | mv-expand resource = report.resources
    | mv-expand reason = resource.reasons
    | project
        resourceName = tostring(resource.resourceId),
        complianceStatus = tostring(resource.complianceStatus),
        reason = tostring(reason.phrase)
    """

    request = QueryRequest(
        subscriptions=[SUBSCRIPTION_ID],
        query=query
    )

    response = client.resources(request)

    print("\n=== P078 BASELINE FINDINGS ===\n")

    findings = []

    for row in response.data:
        finding = {
            "resource": row.get("resourceName"),
            "status": row.get("complianceStatus"),
            "reason": row.get("reason"),
        }

        findings.append(finding)

        print(f"Resource : {finding['resource']}")
        print(f"Status   : {finding['status']}")
        print(f"Reason   : {finding['reason']}")
        print("-" * 70)

    print(f"\nTotal findings extracted: {len(findings)}")

    return findings


if __name__ == "__main__":
    collect_baseline_findings()
