import React from "react";
import { Activity, ShieldCheck } from "lucide-react";

function Header() {
  return (
    <header className="argus-card overflow-hidden">
      <div className="flex flex-col gap-5 border-b border-slate-100 bg-gradient-to-r from-white to-blue-50/40 p-5 sm:p-6 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-start gap-4">
          <div className="rounded-2xl border border-blue-100 bg-white p-3 text-blue-700 shadow-sm">
            <ShieldCheck size={26} strokeWidth={1.9} />
          </div>
          <div>
            <p className="argus-subtitle">Enterprise Command Center</p>
            <h1 className="mt-1.5 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
              ARGUS
            </h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600 sm:text-base">
              Autonomous Risk & Governance for Unified Supply Chain
            </p>
          </div>
        </div>
        <div className="inline-flex w-fit items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700 shadow-sm">
          <Activity size={16} className="fill-emerald-500/20" />
          Live Risk Intelligence
        </div>
      </div>
      <div className="grid gap-4 px-5 py-4 text-sm text-slate-600 sm:grid-cols-3 sm:px-6">
        <div>
          <span className="font-semibold text-slate-950">5000</span> purchase orders analyzed
        </div>
        <div>
          <span className="font-semibold text-slate-950">5</span> vendors under monitoring
        </div>
        <div>
          <span className="font-semibold text-slate-950">PO-00001</span> selected for review
        </div>
      </div>
    </header>
  );
}

export default Header;
