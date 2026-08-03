import React from "react";
import { AlertTriangle, Clock3, Gauge, ShieldCheck } from "lucide-react";

function formatScore(value) {
  return value == null ? "—" : Number(value).toFixed(3);
}

function KpiCards({ kpis, loading }) {
  const cards = [
    {
      label: "Total high-risk POs",
      value: loading ? "…" : kpis.totalHighRisk,
      icon: AlertTriangle
    },
    {
      label: "Average price anomaly",
      value: loading ? "…" : formatScore(kpis.averagePriceAnomaly),
      icon: Gauge
    },
    {
      label: "Average delay probability",
      value: loading ? "…" : formatScore(kpis.averageDelayProbability),
      icon: Clock3
    },
    {
      label: "Selected vendor reliability",
      value: formatScore(kpis.vendorReliability),
      icon: ShieldCheck
    }
  ];

  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map(({ label, value, icon: Icon }) => (
        <article key={label} className="argus-card p-5">
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-sm font-medium text-slate-500">{label}</p>
              <p className="mt-3 text-3xl font-bold text-slate-950">{value}</p>
            </div>
            <div className="rounded-xl bg-blue-50 p-3 text-blue-700">
              <Icon size={22} aria-hidden="true" />
            </div>
          </div>
        </article>
      ))}
    </section>
  );
}

export default KpiCards;
