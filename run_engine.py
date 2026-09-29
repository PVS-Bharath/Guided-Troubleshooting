
import json

from llm_engine import troubleshoot


# Demo-only approved troubleshooting records.
# Replace these with records from your actual retrieval dataset
# before presenting this as production knowledge.
BATTERY_DRAIN_CONTEXT = [
    {
        "source_id": "BATTERY_001",
        "issue": "Phone battery drains quickly",
        "actionName": "Check battery usage",
        "description": "Identify apps consuming unusually high battery power.",
        "category": "manual",
        "steps": [
            "Open Settings.",
            "Open Battery or Battery usage.",
            "Review which apps have used the most battery.",
            "If an app is consuming unusually high power, review its background activity and usage."
        ],
        "deeplink": None
    },
    {
        "source_id": "BATTERY_002",
        "issue": "Phone battery drains quickly",
        "actionName": "Review battery-saving settings",
        "description": "Check whether available power-saving options can reduce battery consumption.",
        "category": "manual",
        "steps": [
            "Open Settings.",
            "Find the Battery section.",
            "Review available power-saving options.",
            "Enable a suitable power-saving option if appropriate."
        ],
        "deeplink": None
    },
    {
        "source_id": "BATTERY_003",
        "issue": "Phone battery drains quickly",
        "actionName": "Check battery condition",
        "description": "Check whether the device reports battery health or service information.",
        "category": "manual",
        "steps": [
            "Open your phone's Settings.",
            "Look for Battery health, Diagnostics, or Device care.",
            "If a battery warning or service recommendation appears, follow the manufacturer's guidance."
        ],
        "deeplink": None
    }
]


def main():
    complaint = input("Describe your issue: ").strip()

    if not complaint:
        print(json.dumps({
            "success": False,
            "error": "Please enter a complaint."
        }, indent=2))
        return

    # Only supply this demo context for a matching battery complaint.
    # Other complaints must use the real retrieval component.
    is_battery_issue = (
        "battery" in complaint.lower()
        and any(word in complaint.lower() for word in ("drain", "drains", "quick", "fast", "die"))
    )

    context = BATTERY_DRAIN_CONTEXT if is_battery_issue else []

    result = troubleshoot(
        complaint,
        retrieved_context=context
    )

    print(json.dumps(
        result,
        indent=2,
        ensure_ascii=False,
        default=str
    ))


if __name__ == "__main__":
    main()