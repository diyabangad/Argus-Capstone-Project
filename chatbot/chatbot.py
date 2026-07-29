import re
from typing import Any

import requests


API_BASE_URL = "http://127.0.0.1:8000"
VENDORS = (
    "Alpha_Inc",
    "Beta_Supplies",
    "Gamma_Co",
    "Delta_Logistics",
    "Epsilon_Group",
)


def call_api(path: str, params: dict[str, Any] | None = None) -> Any:
    try:
        response = requests.get(
            f"{API_BASE_URL}{path}",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError as error:
        raise RuntimeError(
            "I could not connect to the ARGUS backend. "
            "Make sure FastAPI is running on http://127.0.0.1:8000."
        ) from error
    except requests.Timeout as error:
        raise RuntimeError(
            "The ARGUS backend took too long to respond."
        ) from error
    except requests.HTTPError as error:
        raise RuntimeError(
            f"The ARGUS backend returned HTTP {error.response.status_code}."
        ) from error
    except requests.RequestException as error:
        raise RuntimeError(
            f"The ARGUS backend request failed: {error}"
        ) from error
    except ValueError as error:
        raise RuntimeError(
            "The ARGUS backend returned an invalid response."
        ) from error


def detect_vendor(question: str) -> str | None:
    for vendor in VENDORS:
        if re.search(re.escape(vendor), question, flags=re.IGNORECASE):
            return vendor
    return None


def format_high_risk_orders(data: dict[str, Any]) -> str:
    records = data.get("records", [])
    if not records:
        return "No high-risk purchase orders were found."

    lines = [f"I found {len(records)} high-risk purchase orders:"]
    for record in records:
        lines.append(
            f"- {record.get('po_id', 'Unknown PO')} from "
            f"{record.get('supplier', 'Unknown vendor')}: "
            f"price anomaly {record.get('price_anomaly_score', 'N/A')}, "
            f"delay probability {record.get('delay_probability', 'N/A')}."
        )
    return "\n".join(lines)


def format_vendor_profile(data: dict[str, Any], vendor: str) -> str:
    if data.get("message"):
        return f"I could not find a risk profile for {vendor}."

    return (
        f"Risk profile for {data.get('supplier', vendor)}:\n"
        f"- Reliability score: "
        f"{data.get('supplier_reliability_score', 'N/A')}\n"
        f"- Reliability bucket: "
        f"{data.get('supplier_reliability_bucket', 'N/A')}\n"
        f"- Total orders: {data.get('total_orders', 'N/A')}\n"
        f"- Delayed orders: {data.get('delayed_orders', 'N/A')}\n"
        f"- Average price anomaly score: "
        f"{data.get('average_price_anomaly_score', 'N/A')}\n"
        f"- Average delay probability: "
        f"{data.get('average_delay_probability', 'N/A')}"
    )


def format_summary(data: dict[str, Any]) -> str:
    return (
        "ARGUS feature-store summary:\n"
        f"- Vendors: {data.get('total_vendors', 'N/A')}\n"
        f"- Purchase orders: {data.get('total_purchase_orders', 'N/A')}\n"
        f"- Risk scores: {data.get('total_risk_scores', 'N/A')}\n"
        f"- High price-risk orders: "
        f"{data.get('high_price_risk_orders', 'N/A')}\n"
        f"- Delayed orders: {data.get('delayed_orders', 'N/A')}\n"
        f"- Average price anomaly score: "
        f"{data.get('average_price_anomaly_score', 'N/A')}\n"
        f"- Average delay probability: "
        f"{data.get('average_delay_probability', 'N/A')}"
    )


def build_bot_reply(question: str) -> str:
    normalized_question = question.lower()
    vendor = detect_vendor(question)

    try:
        if "high risk" in normalized_question or "high-risk" in normalized_question:
            data = call_api(
                "/api/high-risk-purchase-orders",
                params={"limit": 5},
            )
            return format_high_risk_orders(data)

        if vendor:
            data = call_api(f"/api/vendor-risk-profile/{vendor}")
            return format_vendor_profile(data, vendor)

        if "vendor" in normalized_question and (
            "risk" in normalized_question
            or "profile" in normalized_question
        ):
            return (
                "Please include one of these vendor names: "
                + ", ".join(VENDORS)
                + "."
            )

        if "summary" in normalized_question or "overview" in normalized_question:
            data = call_api("/api/summary")
            return format_summary(data)

        return (
            "I can show high-risk purchase orders, provide a vendor risk "
            "profile, or display the ARGUS summary."
        )
    except RuntimeError as error:
        return str(error)


def main() -> None:
    print("ARGUS Assistant")
    print("Ask about high-risk orders, vendor risk, or summary.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not question:
            continue

        print(f"ARGUS: {build_bot_reply(question)}\n")


if __name__ == "__main__":
    main()
