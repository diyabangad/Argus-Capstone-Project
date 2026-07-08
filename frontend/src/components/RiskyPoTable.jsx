import React from "react";

const flaggedOrders = [
  {
    id: "PO-00001",
    supplier: "Alpha_Inc",
    category: "Office Supplies",
    priceRisk: "0.1339",
    delayRisk: "0.95",
    severity: "Critical",
    action: "Expedite review"
  },
  {
    id: "PO-00042",
    supplier: "Beta_Logistics",
    category: "Packaging",
    priceRisk: "0.1182",
    delayRisk: "0.89",
    severity: "High",
    action: "Vendor follow-up"
  },
  {
    id: "PO-00137",
    supplier: "Delta_Trade",
    category: "IT Hardware",
    priceRisk: "0.0924",
    delayRisk: "0.81",
    severity: "High",
    action: "Validate quote"
  },
  {
    id: "PO-00318",
    supplier: "Northstar_Supply",
    category: "Facilities",
    priceRisk: "0.0761",
    delayRisk: "0.74",
    severity: "Medium",
    action: "Monitor"
  }
];

function severityClass(severity) {
  if (severity === "Critical") {
    return "border-red-100 bg-red-50 text-red-700";
  }

  if (severity === "High") {
    return "border-blue-100 bg-blue-50 text-blue-700";
  }

  return "border-slate-200 bg-slate-50 text-slate-700";
}

function RiskyPoTable() {
  return (
    <section className="argus-card overflow-hidden">
      <div className="flex flex-col gap-2 border-b border-slate-100 p-5 sm:p-6">
        <p className="argus-subtitle">Risk Queue</p>
        <h2 className="text-xl font-semibold tracking-tight text-slate-950">Flagged Purchase Orders</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[820px] text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-[0.14em] text-slate-500">
            <tr>
              <th className="px-5 py-4 font-semibold">PO ID</th>
              <th className="px-5 py-4 font-semibold">Supplier</th>
              <th className="px-5 py-4 font-semibold">Category</th>
              <th className="px-5 py-4 font-semibold">Price Risk</th>
              <th className="px-5 py-4 font-semibold">Delay Risk</th>
              <th className="px-5 py-4 font-semibold">Severity</th>
              <th className="px-5 py-4 font-semibold">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {flaggedOrders.map((order) => (
              <tr key={order.id} className="transition hover:bg-slate-50/80">
                <td className="px-5 py-4 font-semibold text-slate-950">{order.id}</td>
                <td className="px-5 py-4 text-slate-800">{order.supplier}</td>
                <td className="px-5 py-4 text-slate-500">{order.category}</td>
                <td className="px-5 py-4 font-medium text-slate-800">{order.priceRisk}</td>
                <td className="px-5 py-4 font-medium text-slate-800">{order.delayRisk}</td>
                <td className="px-5 py-4">
                  <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${severityClass(order.severity)}`}>
                    {order.severity}
                  </span>
                </td>
                <td className="px-5 py-4 text-slate-800">{order.action}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default RiskyPoTable;
