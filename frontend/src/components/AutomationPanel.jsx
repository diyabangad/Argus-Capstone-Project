import React, { useEffect, useState } from "react";
import { Bot, Send } from "lucide-react";

const LIVE_PO_ERROR =
  "I could not load live purchase order data right now. Please confirm the backend is running and try again.";

function toNumber(value) {
  const numericValue = Number(value);
  return Number.isFinite(numericValue) ? numericValue : null;
}

function formatScore(value) {
  const numericValue = toNumber(value);
  return numericValue === null ? "Not available" : numericValue.toFixed(3);
}

function riskRank(order) {
  const priceRisk = toNumber(order.price_anomaly_score);
  const delayRisk = toNumber(order.delay_probability);
  return (priceRisk ?? 0) + (delayRisk ?? 0);
}

function getRiskReason(order) {
  const priceRisk = toNumber(order.price_anomaly_score);
  const delayRisk = toNumber(order.delay_probability);

  if ((delayRisk ?? 0) >= 0.75 && (priceRisk ?? 0) >= 0.5) {
    return "Delay probability and price anomaly score are both high.";
  }

  if ((delayRisk ?? 0) >= 0.75) {
    return "Delay probability is high.";
  }

  if ((priceRisk ?? 0) >= 0.5) {
    return "Price anomaly score is high.";
  }

  return "This PO appears in the backend high-risk queue.";
}

function getRecommendedAction(order) {
  const priceRisk = toNumber(order.price_anomaly_score);
  const delayRisk = toNumber(order.delay_probability);

  if ((delayRisk ?? 0) >= 0.75 && (priceRisk ?? 0) >= 0.5) {
    return "Hold the PO temporarily, escalate to procurement leadership, review the supplier, and prepare a backup vendor option.";
  }

  if ((delayRisk ?? 0) >= 0.75) {
    return "Review supplier lead time, confirm shipment readiness, and consider expedited shipment or rerouting to a backup supplier.";
  }

  if ((priceRisk ?? 0) >= 0.5) {
    return "Review the price anomaly, compare negotiated price against history, and consider renegotiation.";
  }

  return "Review the PO details and confirm supplier status before approval.";
}

function sortByRisk(orders) {
  return [...orders].sort((a, b) => riskRank(b) - riskRank(a));
}

function formatPoSummary(order, index) {
  return `${index + 1}. ${order.po_id} - ${order.supplier}
   Price anomaly score: ${formatScore(order.price_anomaly_score)}
   Delay probability: ${formatScore(order.delay_probability)}
   Reason: ${getRiskReason(order)}
   Recommended action: ${getRecommendedAction(order)}`;
}

function matchesAny(text, keywords) {
  return keywords.some((keyword) => text.includes(keyword));
}

function getAssistantIntent(message) {
  const normalized = message.toLowerCase();

  if (
    matchesAny(normalized, [
      "highest-risk",
      "highest risk",
      "riskiest",
      "recommend action",
      "what action",
      "what should i do"
    ])
  ) {
    return "highestRiskAction";
  }

  if (
    matchesAny(normalized, [
      "immediate attention",
      "show high risk",
      "high-risk",
      "high risk",
      "highest risk",
      "which pos",
      "which purchase orders",
      "review first",
      "orders should we review"
    ])
  ) {
    return "topRiskOrders";
  }

  if (matchesAny(normalized, ["delay", "shipment", "late", "eta"])) {
    return "delayAction";
  }

  return "topRiskOrders";
}

function buildTopRiskReply(orders) {
  const topOrders = sortByRisk(orders).slice(0, 3);

  return `Immediate attention required:
${topOrders.map(formatPoSummary).join("\n\n")}`;
}

function buildActionReply(order, heading = "Recommended action for the highest-risk PO") {
  return `${heading}:
${order.po_id} - ${order.supplier}
Price anomaly score: ${formatScore(order.price_anomaly_score)}
Delay probability: ${formatScore(order.delay_probability)}
Reason: ${getRiskReason(order)}
Recommended action: ${getRecommendedAction(order)}`;
}

async function loadHighRiskOrders() {
  const response = await fetch("/api/high-risk-purchase-orders?limit=20");

  if (!response.ok) {
    throw new Error(`High-risk PO request failed with ${response.status}`);
  }

  const body = await response.json();
  return Array.isArray(body.records) ? body.records : [];
}

function AutomationPanel({ selectedOrder }) {
  const [payload, setPayload] = useState(null);
  const [message, setMessage] = useState("What should I do about this delay?");
  const [reply, setReply] = useState("The assistant is ready to guide your next action.");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!selectedOrder) return;

    async function loadAutomationPayload() {
      setLoading(true);
      try {
        const response = await fetch("/api/automation/payload", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            po_id: selectedOrder.po_id,
            supplier: selectedOrder.supplier,
            item_category: selectedOrder.item_category,
            anomaly_score: selectedOrder.price_anomaly_score,
            delay_probability: selectedOrder.delay_probability,
          }),
        });

        if (!response.ok) {
          throw new Error(`Automation payload failed with ${response.status}`);
        }

        const body = await response.json();
        setPayload(body);
      } catch (error) {
        setPayload({
          po_id: selectedOrder.po_id,
          priority: "medium",
          sap_actions: [{ action: "review", description: "Review manually" }],
        });
      } finally {
        setLoading(false);
      }
    }

    loadAutomationPayload();
  }, [selectedOrder]);

  async function handleAsk() {
    try {
      const orders = await loadHighRiskOrders();

      if (!orders.length) {
        setReply(LIVE_PO_ERROR);
        return;
      }

      const sortedOrders = sortByRisk(orders);
      const highestRiskOrder = sortedOrders[0];
      const selectedLiveOrder = selectedOrder
        ? orders.find((order) => order.po_id === selectedOrder.po_id)
        : null;
      const intent = getAssistantIntent(message);

      if (intent === "topRiskOrders") {
        setReply(buildTopRiskReply(sortedOrders));
        return;
      }

      if (intent === "delayAction") {
        setReply(buildActionReply(selectedLiveOrder || highestRiskOrder, "Delay-risk guidance"));
        return;
      }

      setReply(buildActionReply(highestRiskOrder));
    } catch (error) {
      setReply(LIVE_PO_ERROR);
    }
  }

  return (
    <section className="argus-card p-5 sm:p-6">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-950">ARGUS Automation & Assistant</h2>
          <p className="mt-1 text-sm text-slate-500">
            Generate a SAP-friendly payload and ask the assistant for guidance.
          </p>
        </div>
        <div className="rounded-2xl border border-blue-100 bg-blue-50 p-3 text-blue-700">
          <Bot size={20} />
        </div>
      </div>

      <div className="mt-5 grid gap-4 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <h3 className="text-sm font-semibold text-slate-900">Automation payload</h3>
          {loading ? (
            <p className="mt-3 text-sm text-slate-500">Generating payload…</p>
          ) : (
            <div className="mt-3 space-y-2 text-sm text-slate-700">
              <p><span className="font-semibold">PO:</span> {payload?.po_id ?? "—"}</p>
              <p><span className="font-semibold">Priority:</span> {payload?.priority ?? "—"}</p>
              <p><span className="font-semibold">Supplier:</span> {payload?.supplier ?? "—"}</p>
              <div>
                <span className="font-semibold">SAP actions:</span>
                <ul className="mt-2 list-disc pl-5">
                  {(payload?.sap_actions ?? []).map((action) => (
                    <li key={action.action}>{action.description}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>

        <div className="rounded-2xl border border-slate-200 bg-white p-4">
          <h3 className="text-sm font-semibold text-slate-900">Assistant</h3>
          <p className="mt-2 whitespace-pre-line text-sm text-slate-600">{reply}</p>
          <div className="mt-4 flex items-center gap-2">
            <input
              className="flex-1 rounded-lg border border-slate-200 px-3 py-2 text-sm outline-none focus:border-blue-500"
              value={message}
              onChange={(event) => setMessage(event.target.value)}
              placeholder="Ask the assistant"
            />
            <button
              onClick={handleAsk}
              className="rounded-lg bg-blue-600 p-2 text-white"
              aria-label="Ask assistant"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default AutomationPanel;
