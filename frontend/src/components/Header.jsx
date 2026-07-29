import React from "react";
import { ShieldCheck } from "lucide-react";

function Header() {
  return (
    <header className="argus-card flex flex-col gap-4 p-6 sm:flex-row sm:items-center">
      <div className="w-fit rounded-xl bg-blue-600 p-3 text-white">
        <ShieldCheck size={28} aria-hidden="true" />
      </div>
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">
          ARGUS — Supply Chain Risk Intelligence
        </h1>
        <p className="mt-1 text-sm text-slate-500 sm:text-base">
          Monitor high-risk purchase orders and supplier performance.
        </p>
      </div>
    </header>
  );
}

export default Header;
