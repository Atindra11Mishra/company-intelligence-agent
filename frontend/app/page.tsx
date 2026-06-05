"use client";

import { useState } from "react";

import CompanySearchForm from "@/components/CompanySearchForm";
import AgentTrace from "@/components/AgentTrace";
import ReportViewer from "@/components/ReportViewer";
import SourceList from "@/components/SourceList";
import LoadingState from "@/components/LoadingState";

import { researchCompany } from "@/lib/api";
import type { ResearchResponse } from "@/lib/types";

export default function HomePage() {
  const [result, setResult] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleResearch(companyInput: string) {
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await researchCompany(companyInput);
      setResult(data);
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Something went wrong while generating the report.";

      setError(message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="border-b border-slate-900 bg-gradient-to-b from-slate-900 to-slate-950 px-4 py-16">
        <div className="mx-auto max-w-6xl text-center">
          <div className="mb-5 inline-flex rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-2 text-sm text-blue-300">
            LangGraph-powered company research agent
          </div>

          <h1 className="mx-auto max-w-4xl text-4xl font-bold tracking-tight text-white md:text-6xl">
            Company Intelligence Agent
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-slate-400 md:text-lg">
            Enter a company name, website, or LinkedIn link. The agent researches
            overview, funding, leadership, competitors, news, hiring trends, and
            tech stack signals, then generates a structured intelligence report.
          </p>

          <div className="mt-10">
            <CompanySearchForm
              onSubmit={handleResearch}
              isLoading={isLoading}
            />
          </div>

          <div className="mt-5 flex flex-wrap justify-center gap-2 text-xs text-slate-500">
            <span className="rounded-full border border-slate-800 px-3 py-1">
              FastAPI
            </span>
            <span className="rounded-full border border-slate-800 px-3 py-1">
              LangGraph
            </span>
            <span className="rounded-full border border-slate-800 px-3 py-1">
              Tavily
            </span>
            <span className="rounded-full border border-slate-800 px-3 py-1">
              Groq
            </span>
          </div>
        </div>
      </section>

      <section className="px-4 py-10">
        <div className="mx-auto max-w-6xl">
          {isLoading && <LoadingState />}

          {error && (
            <div className="mx-auto max-w-3xl rounded-2xl border border-red-500/30 bg-red-500/10 p-5 text-red-200">
              <h2 className="font-semibold">Research failed</h2>
              <p className="mt-1 text-sm">{error}</p>
            </div>
          )}

          {!isLoading && !error && !result && (
            <div className="mx-auto max-w-3xl rounded-2xl border border-slate-800 bg-slate-950 p-6 text-center">
              <h2 className="text-lg font-semibold text-slate-100">
                Try a company search
              </h2>
              <p className="mt-2 text-sm text-slate-400">
                Example: Stripe, Perplexity AI, Notion, Razorpay, OpenAI,
                Anthropic.
              </p>
            </div>
          )}

          {result && (
            <div className="grid gap-6 lg:grid-cols-[360px_1fr]">
              <div className="space-y-6">
                <AgentTrace trace={result.agent_trace} />
                <SourceList sources={result.sources} />
              </div>

              <ReportViewer markdown={result.report_markdown} />
            </div>
          )}
        </div>
      </section>
    </main>
  );
}