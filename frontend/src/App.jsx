import React, { useEffect, useMemo, useState } from "react";
import Header from "./components/Header.jsx";
import KpiCards from "./components/KpiCards.jsx";
import RiskyPoTable from "./components/RiskyPoTable.jsx";
import VendorProfile from "./components/VendorProfile.jsx";
import AutomationPanel from "./components/AutomationPanel.jsx";

const vendors = [
  "Alpha_Inc",
  "Beta_Supplies",
  "Gamma_Co",
  "Delta_Logistics",
  "Epsilon_Group"
];

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Backend returned HTTP ${response.status}`);
  }
  return response.json();
}

function App() {
  const [orders, setOrders] = useState([]);
  const [ordersLoading, setOrdersLoading] = useState(true);
  const [ordersError, setOrdersError] = useState("");
  const [selectedVendor, setSelectedVendor] = useState(vendors[0]);
  const [vendorProfile, setVendorProfile] = useState(null);
  const [vendorLoading, setVendorLoading] = useState(true);
  const [vendorError, setVendorError] = useState("");

  useEffect(() => {
    async function loadOrders() {
      setOrdersLoading(true);
      setOrdersError("");
      try {
        const data = await fetchJson(
          "/api/high-risk-purchase-orders?limit=20"
        );
        setOrders(data.records ?? []);
      } catch (error) {
        setOrdersError(
          `${error.message}. Make sure the ARGUS backend is running on port 8000.`
        );
      } finally {
        setOrdersLoading(false);
      }
    }

    loadOrders();
  }, []);

  useEffect(() => {
    async function loadVendorProfile() {
      setVendorLoading(true);
      setVendorError("");
      setVendorProfile(null);
      try {
        const data = await fetchJson(
          `/api/vendor-risk-profile/${selectedVendor}`
        );
        if (data.message) {
          throw new Error(data.message);
        }
        setVendorProfile(data);
      } catch (error) {
        setVendorError(
          `${error.message}. Make sure the ARGUS backend is running and the feature store is loaded.`
        );
      } finally {
        setVendorLoading(false);
      }
    }

    loadVendorProfile();
  }, [selectedVendor]);

  const kpis = useMemo(() => {
    const average = (field) => {
      const values = orders
        .map((order) => Number(order[field]))
        .filter(Number.isFinite);
      if (!values.length) return null;
      return values.reduce((sum, value) => sum + value, 0) / values.length;
    };

    return {
      totalHighRisk: orders.length,
      averagePriceAnomaly: average("price_anomaly_score"),
      averageDelayProbability: average("delay_probability"),
      vendorReliability: vendorProfile?.supplier_reliability_score ?? null
    };
  }, [orders, vendorProfile]);

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-6 text-slate-900 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-6">
        <Header />
        <KpiCards kpis={kpis} loading={ordersLoading} />
        <VendorProfile
          vendors={vendors}
          selectedVendor={selectedVendor}
          onVendorChange={setSelectedVendor}
          profile={vendorProfile}
          loading={vendorLoading}
          error={vendorError}
        />
        <AutomationPanel selectedOrder={orders[0]} />
        <RiskyPoTable
          orders={orders}
          loading={ordersLoading}
          error={ordersError}
        />
      </div>
    </main>
  );
}

export default App;
