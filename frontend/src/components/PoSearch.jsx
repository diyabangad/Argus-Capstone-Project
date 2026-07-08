import React from "react";
import { Search } from "lucide-react";

function PoSearch({ purchaseOrder }) {
  return (
    <section className="argus-card p-5 sm:p-6">
      <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="argus-subtitle">Purchase Order Lookup</p>
          <h2 className="mt-2 text-xl font-semibold tracking-tight text-slate-950">PO search</h2>
          <p className="mt-1.5 text-sm leading-6 text-slate-500">
            Static preview for {purchaseOrder.supplier} risk scoring.
          </p>
        </div>
        <div className="flex w-full flex-col gap-3 sm:flex-row lg:max-w-xl">
          <label className="sr-only" htmlFor="po-search">
            Purchase order ID
          </label>
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-argus-muted" size={18} />
            <input
              id="po-search"
              type="text"
              placeholder="PO-00001"
              defaultValue={purchaseOrder.id}
              className="h-12 w-full rounded-xl border border-slate-200 bg-slate-50/60 pl-11 pr-4 text-sm font-semibold text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:bg-white focus:ring-4 focus:ring-blue-100"
            />
          </div>
          <button className="h-12 rounded-xl bg-blue-700 px-5 text-sm font-semibold text-white shadow-sm shadow-blue-700/20 transition hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-100">
            Check Risk
          </button>
        </div>
      </div>
    </section>
  );
}

export default PoSearch;
