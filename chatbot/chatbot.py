import re
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"


def extract_po_id(text: str):
    match = re.search(r"PO-\d+", text.upper())
    return match.group(0) if match else None


def get_summary():
    response = requests.get(f"{API_BASE_URL}/api/summary")
    response.raise_for_status()
    return response.json()


def get_price_risk(po_id: str):
    response = requests.get(
        f"{API_BASE_URL}/api/price-risk",
        params={"po_id": po_id}
    )
    response.raise_for_status()
    return response.json()


def get_delay_risk(po_id: str):
    response = requests.get(
        f"{API_BASE_URL}/api/delay-risk",
        params={"po_id": po_id}
    )
    response.raise_for_status()
    return response.json()


def build_bot_reply(user_question: str):
    question = user_question.lower()
    po_id = extract_po_id(user_question)

    try:
        if "summary" in question or "overview" in question or "total" in question:
            data = get_summary()
            return (
                f"ARGUS analysed {data['total_purchase_orders']} purchase orders.\n\n"
                f"- High price-risk orders: {data['high_price_risk_orders']}\n"
                f"- High delay-risk orders: {data['high_delay_risk_orders']}"
            )

        if po_id and ("price" in question or "anomaly" in question):
            data = get_price_risk(po_id)
            return (
                f"Price risk result for {data['po_id']}:\n\n"
                f"- Supplier: {data['supplier']}\n"
                f"- Item category: {data['item_category']}\n"
                f"- Is price anomaly: {data['is_anomaly']}\n"
                f"- Anomaly score: {data['anomaly_score']}"
            )

        if po_id and ("delay" in question or "late" in question):
            data = get_delay_risk(po_id)
            return (
                f"Delay risk result for {data['po_id']}:\n\n"
                f"- Supplier: {data['supplier']}\n"
                f"- Item category: {data['item_category']}\n"
                f"- Delay probability: {data['delay_probability']}\n"
                f"- Predicted delay days: {data['predicted_delay_days']}"
            )

        if po_id:
            price_data = get_price_risk(po_id)
            delay_data = get_delay_risk(po_id)

            return (
                f"Risk summary for {po_id}:\n\n"
                f"Price risk:\n"
                f"- Is anomaly: {price_data['is_anomaly']}\n"
                f"- Anomaly score: {price_data['anomaly_score']}\n\n"
                f"Delay risk:\n"
                f"- Delay probability: {delay_data['delay_probability']}\n"
                f"- Predicted delay days: {delay_data['predicted_delay_days']}\n\n"
                f"Supplier: {price_data['supplier']}\n"
                f"Item category: {price_data['item_category']}"
            )

        return (
            "I can answer questions like:\n\n"
            "- Give me project summary\n"
            "- Check price risk for PO-00001\n"
            "- Check delay risk for PO-00001\n"
            "- Show risk for PO-00001"
        )

    except Exception as error:
        return f"Something went wrong while calling the backend API: {error}"


st.set_page_config(
    page_title="ARGUS Assistant",
    page_icon="🛡️",
    layout="centered"
)

st.title("ARGUS Assistant")
st.caption("Procurement and supply-chain risk chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi, I am ARGUS Assistant. Ask me about procurement price risk, delay risk, or summary."
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask about PO risk, delay, price anomaly, or summary...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    bot_reply = build_bot_reply(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    with st.chat_message("assistant"):
        st.write(bot_reply)