import React from "react";
import { Bot, Send } from "lucide-react";

function AssistantPreview({ purchaseOrder }) {
  return (
    <aside className="argus-card flex min-h-[520px] flex-col p-5 sm:p-6">
      <div className="flex items-center gap-3 border-b border-slate-100 pb-5">
        <div className="rounded-2xl border border-blue-100 bg-blue-50 p-3 text-blue-700 shadow-sm">
          <Bot size={22} strokeWidth={2} />
        </div>
        <div>
          <p className="text-sm font-semibold text-slate-950">ARGUS Assistant</p>
          <p className="text-xs text-slate-500">Preview only, not connected</p>
        </div>
      </div>

      <div className="flex flex-1 flex-col gap-4 py-5">
        <div className="max-w-[88%] rounded-2xl rounded-tl-md border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-700 shadow-sm">
          Monitoring {purchaseOrder.id} for supplier {purchaseOrder.supplier}. Delay probability is elevated at{" "}
          {purchaseOrder.delayProbability.toFixed(2)}.
        </div>
        <div className="ml-auto max-w-[88%] rounded-2xl rounded-tr-md bg-blue-700 p-4 text-sm leading-6 text-white shadow-sm shadow-blue-700/20">
          What action should procurement take first?
        </div>
        <div className="max-w-[88%] rounded-2xl rounded-tl-md border border-blue-100 bg-blue-50 p-4 text-sm leading-6 text-slate-700 shadow-sm">
          Confirm dispatch availability, request an updated fulfillment date, and hold price approval for secondary review.
        </div>
      </div>

      <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 shadow-sm">
        <span className="flex-1 text-sm text-slate-500">Ask about a flagged purchase order</span>
        <button className="rounded-lg bg-blue-50 p-2 text-blue-700 transition hover:bg-blue-100" aria-label="Preview send">
          <Send size={16} />
        </button>
      </div>
    </aside>
  );
}

export default AssistantPreview;
