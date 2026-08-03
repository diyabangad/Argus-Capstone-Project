import React from "react";

function formatScore(value) {
  return value == null ? "—" : Number(value).toFixed(3);
}

function VendorProfile({
  vendors,
  selectedVendor,
  onVendorChange,
  profile,
  loading,
  error
}) {
  return (
    <section className="argus-card p-5 sm:p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-slate-950">
            Vendor risk profile
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Select a supplier to review reliability and delivery performance.
          </p>
        </div>
        <label className="text-sm font-medium text-slate-700">
          Vendor
          <select
            className="mt-1 block w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 sm:w-56"
            value={selectedVendor}
            onChange={(event) => onVendorChange(event.target.value)}
          >
            {vendors.map((vendor) => (
              <option key={vendor} value={vendor}>
                {vendor}
              </option>
            ))}
          </select>
        </label>
      </div>

      {loading && (
        <p className="mt-6 text-sm text-slate-500">Loading vendor profile…</p>
      )}
      {error && (
        <p className="mt-6 rounded-lg bg-red-50 p-4 text-sm text-red-700">
          {error}
        </p>
      )}
      {!loading && !error && profile && (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
          <ProfileValue label="Supplier" value={profile.supplier} />
          <ProfileValue
            label="Reliability"
            value={formatScore(profile.supplier_reliability_score)}
          />
          <ProfileValue
            label="Reliability bucket"
            value={profile.supplier_reliability_bucket ?? "—"}
          />
          <ProfileValue label="Total orders" value={profile.total_orders} />
          <ProfileValue label="Delayed orders" value={profile.delayed_orders} />
        </div>
      )}
    </section>
  );
}

function ProfileValue({ label, value }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-2 font-semibold text-slate-950">{value}</p>
    </div>
  );
}

export default VendorProfile;
