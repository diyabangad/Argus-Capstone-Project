import React from "react";
import Header from "./components/Header.jsx";
import KpiCards from "./components/KpiCards.jsx";
import PoSearch from "./components/PoSearch.jsx";
import RiskDetailCards from "./components/RiskDetailCards.jsx";
import RiskyPoTable from "./components/RiskyPoTable.jsx";
import AssistantPreview from "./components/AssistantPreview.jsx";

const selectedPurchaseOrder = {
  id: "PO-00001",
  supplier: "Alpha_Inc",
  category: "Office Supplies",
  priceAnomalyScore: 0.1339,
  delayProbability: 0.95,
  predictedDelayDays: 0.97,
  severity: "Critical"
};

function App() {
  return (
    <main className="min-h-screen bg-[#f8fafc] px-4 py-5 text-slate-900 sm:px-6 lg:px-8 lg:py-7">
      <div className="mx-auto flex max-w-7xl flex-col gap-5">
        <Header />
        <KpiCards />
        <div className="grid gap-5 xl:grid-cols-[minmax(0,1fr)_380px]">
          <div className="flex flex-col gap-5">
            <PoSearch purchaseOrder={selectedPurchaseOrder} />
            <RiskDetailCards purchaseOrder={selectedPurchaseOrder} />
            <RiskyPoTable />
          </div>
          <AssistantPreview purchaseOrder={selectedPurchaseOrder} />
        </div>
      </div>
    </main>
  );
}

export default App;
