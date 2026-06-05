import { CheckCircle2, CircleAlert, Clock } from "lucide-react";
import type { AgentTraceItem } from "@/lib/types";

type AgentTraceProps = {
  trace: AgentTraceItem[];
};

function getConfidenceClass(confidence?: string) {
  if (confidence === "High") {
    return "border-emerald-500/30 bg-emerald-500/10 text-emerald-300";
  }

  if (confidence === "Medium") {
    return "border-amber-500/30 bg-amber-500/10 text-amber-300";
  }

  if (confidence === "Low") {
    return "border-red-500/30 bg-red-500/10 text-red-300";
  }

  return "border-slate-700 bg-slate-800 text-slate-300";
}

export default function AgentTrace({ trace }: AgentTraceProps) {
  if (!trace.length) return null;

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-950 p-5">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Agent Trace</h2>
          <p className="text-sm text-slate-400">
            Completed research steps from the LangGraph workflow.
          </p>
        </div>

        <span className="rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-xs text-slate-300">
          {trace.length} steps
        </span>
      </div>

      <div className="space-y-3">
        {trace.map((item, index) => (
          <div
            key={`${item.agent}-${index}`}
            className="flex gap-3 rounded-xl border border-slate-800 bg-slate-900/60 p-4"
          >
            <div className="mt-0.5">
              {item.status === "completed" ? (
                <CheckCircle2 className="h-5 w-5 text-emerald-400" />
              ) : item.status === "failed" ? (
                <CircleAlert className="h-5 w-5 text-red-400" />
              ) : (
                <Clock className="h-5 w-5 text-slate-400" />
              )}
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="font-medium capitalize text-slate-100">
                  {item.agent.replaceAll("_", " ")}
                </h3>

                {item.confidence && (
                  <span
                    className={`rounded-full border px-2 py-0.5 text-xs ${getConfidenceClass(
                      item.confidence
                    )}`}
                  >
                    {item.confidence}
                  </span>
                )}

                {typeof item.sources_found === "number" && (
                  <span className="rounded-full border border-slate-700 bg-slate-800 px-2 py-0.5 text-xs text-slate-300">
                    {item.sources_found} sources
                  </span>
                )}
              </div>

              {item.message && (
                <p className="mt-1 text-sm text-slate-400">{item.message}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}