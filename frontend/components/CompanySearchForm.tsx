"use client";

import { FormEvent, useState } from "react";
import { Search } from "lucide-react";

type CompanySearchFormProps = {
  onSubmit: (companyInput: string) => void;
  isLoading: boolean;
};

export default function CompanySearchForm({
  onSubmit,
  isLoading,
}: CompanySearchFormProps) {
  const [companyInput, setCompanyInput] = useState("");

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedInput = companyInput.trim();

    if (!trimmedInput) return;

    onSubmit(trimmedInput);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto flex w-full max-w-3xl flex-col gap-4 rounded-2xl border border-slate-800 bg-slate-950/70 p-4 shadow-2xl shadow-slate-950/40 backdrop-blur md:flex-row"
    >
      <div className="relative flex-1">
        <Search className="pointer-events-none absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-500" />

        <input
          type="text"
          value={companyInput}
          onChange={(event) => setCompanyInput(event.target.value)}
          placeholder="Enter company name, URL, or LinkedIn link"
          className="w-full rounded-xl border border-slate-800 bg-slate-900 px-12 py-4 text-sm text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-blue-500"
          disabled={isLoading}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="rounded-xl bg-blue-600 px-6 py-4 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-400"
      >
        {isLoading ? "Generating report..." : "Generate Report"}
      </button>
    </form>
  );
}