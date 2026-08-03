import React, { useEffect, useState } from "react";
import { Bot, Send } from "lucide-react";

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
      const response = await fetch("/api/chatbot/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`Chatbot failed with ${response.status}`);
      }

      const body = await response.json();
      setReply(body.reply || "The assistant is ready to help.");
    } catch (error) {
      setReply("The assistant is currently unavailable, but the workflow is queued for review.");
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
          <p className="mt-2 text-sm text-slate-600">{reply}</p>
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
