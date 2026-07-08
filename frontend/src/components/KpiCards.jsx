import React from "react";
import { AlertTriangle, Building2, Clock3, FileText } from "lucide-react";

const kpis = [
  {
    label: "Total Purchase Orders",
    value: "5000",
    helper: "Active procurement records",
    icon: FileText
  },
  {
    label: "High Price Risk Orders",
    value: "721",
    helper: "Marked by anomaly scoring",
    icon: AlertTriangle
  },
  {
    label: "High Delay Risk Orders",
    value: "5000",
    helper: "Require timeline monitoring",
    icon: Clock3
  },
  {
    label: "Vendors Monitored",
    value: "5",
    helper: "Across supplier network",
    icon: Building2
  }
];

function KpiCards() {
  return (
    <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
      {kpis.map((kpi) => {
        const Icon = kpi.icon;
        return (
          <article key={kpi.label} className="argus-card p-5 transition hover:-translate-y-0.5 hover:shadow-xl">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-semibold text-slate-600">{kpi.label}</p>
                <p className="mt-3 text-3xl font-bold tracking-tight text-slate-950">{kpi.value}</p>
              </div>
              <div className="rounded-2xl border border-blue-100 bg-blue-50 p-3 text-blue-700 shadow-sm">
                <Icon size={24} strokeWidth={2} />
              </div>
            </div>
            <div className="mt-5 h-1.5 rounded-full bg-slate-100">
              <div className="h-1.5 w-2/3 rounded-full bg-blue-600" />
            </div>
            <p className="mt-4 text-sm leading-6 text-slate-500">{kpi.helper}</p>
          </article>
        );
      })}
    </section>
  );
}

export default KpiCards;
