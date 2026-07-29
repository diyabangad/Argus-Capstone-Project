import React from "react";

function formatScore(value) {
  return value == null ? "—" : Number(value).toFixed(3);
}

function RiskyPoTable({ orders, loading, error }) {
  return (
    <section className="argus-card overflow-hidden">
      <div className="border-b border-slate-200 p-5 sm:p-6">
        <h2 className="text-xl font-semibold text-slate-950">
          High-risk purchase orders
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Showing up to 20 orders flagged for price or delivery risk.
        </p>
      </div>

      {loading && (
        <p className="p-6 text-sm text-slate-500">Loading purchase orders…</p>
      )}
      {error && (
        <p className="m-5 rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {error}
        </p>
      )}
      {!loading && !error && orders.length === 0 && (
        <p className="p-6 text-sm text-slate-500">
          No high-risk purchase orders were found.
        </p>
      )}

      {!loading && !error && orders.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1050px] text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-5 py-4">PO ID</th>
                <th className="px-5 py-4">Supplier</th>
                <th className="px-5 py-4">Category</th>
                <th className="px-5 py-4">Quantity</th>
                <th className="px-5 py-4">Price anomaly score</th>
                <th className="px-5 py-4">Delay probability</th>
                <th className="px-5 py-4">Recommended note</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {orders.map((order) => (
                <tr key={order.po_id} className="hover:bg-slate-50">
                  <td className="px-5 py-4 font-semibold">{order.po_id}</td>
                  <td className="px-5 py-4">{order.supplier}</td>
                  <td className="px-5 py-4">{order.item_category ?? "—"}</td>
                  <td className="px-5 py-4">{order.quantity ?? "—"}</td>
                  <td className="px-5 py-4">
                    {formatScore(order.price_anomaly_score)}
                  </td>
                  <td className="px-5 py-4">
                    {formatScore(order.delay_probability)}
                  </td>
                  <td className="max-w-xs px-5 py-4 text-slate-600">
                    {order.recommended_note ?? "Review this purchase order."}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

export default RiskyPoTable;
