import React from "react";
import { BadgeAlert, Factory, LineChart, Wand2 } from "lucide-react";

function RiskDetailCards({ purchaseOrder }) {
  const cards = [
    {
      title: "Price Risk Analysis",
      icon: LineChart,
      value: purchaseOrder.priceAnomalyScore.toFixed(4),
      label: "Price anomaly score",
      detail: "Moderate variance detected against peer office supply orders.",
      badge: "Review"
    },
    {
      title: "Delay Risk Analysis",
      icon: BadgeAlert,
      value: `${Math.round(purchaseOrder.delayProbability * 100)}%`,
      label: "Delay probability",
      detail: `Predicted delay window is ${purchaseOrder.predictedDelayDays.toFixed(2)} days.`,
      badge: "Elevated"
    },
    {
      title: "Supplier Profile",
      icon: Factory,
      value: purchaseOrder.supplier,
      label: purchaseOrder.category,
      detail: "Stable vendor history with elevated near-term delivery exposure.",
      badge: "Monitored"
    },
    {
      title: "Remediation Recommendation",
      icon: Wand2,
      value: "Expedite review",
      label: "Recommended action",
      detail: "Confirm inventory availability and request updated dispatch confirmation.",
      badge: "Recommended"
    }
  ];

  return (
    <section className="grid gap-4 md:grid-cols-2">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <article key={card.title} className="argus-card p-5 sm:p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-950">{card.title}</p>
                <p className="mt-4 text-3xl font-bold tracking-tight text-slate-950">{card.value}</p>
                <p className="mt-1 text-sm text-slate-500">{card.label}</p>
              </div>
              <div className="rounded-2xl border border-blue-100 bg-blue-50 p-3 text-blue-700 shadow-sm">
                <Icon size={22} strokeWidth={2} />
              </div>
            </div>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <span className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                {card.badge}
              </span>
              <p className="text-sm leading-6 text-slate-500">{card.detail}</p>
            </div>
          </article>
        );
      })}
    </section>
  );
}

export default RiskDetailCards;
