"use client";

import { useEffect, useState } from "react";
import { Loader2, Search, Newspaper, BriefcaseBusiness, Cpu, FileText } from "lucide-react";

function formatElapsedTime(seconds: number) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  if (minutes === 0) {
    return `${remainingSeconds}s`;
  }

  return `${minutes}m ${remainingSeconds}s`;
}

export default function LoadingState() {
  const [elapsedSeconds, setElapsedSeconds] = useState(0);

  useEffect(() => {
    const intervalId = window.setInterval(() => {
      setElapsedSeconds((previous) => previous + 1);
    }, 1000);

    return () => window.clearInterval(intervalId);
  }, []);

  const steps = [
    {
      label: "Discovering company sources",
      icon: Search,
    },
    {
      label: "Checking funding, leadership, and competitors",
      icon: BriefcaseBusiness,
    },
    {
      label: "Scanning recent news and announcements",
      icon: Newspaper,
    },
    {
      label: "Reading hiring and tech stack signals",
      icon: Cpu,
    },
    {
      label: "Generating final intelligence report",
      icon: FileText,
    },
  ];

  return (
    <div className="mx-auto mt-10 max-w-3xl rounded-2xl border border-slate-800 bg-slate-950 p-6 shadow-2xl shadow-slate-950/40">
      <div className="flex items-start gap-4">
        <div className="rounded-xl border border-blue-500/30 bg-blue-500/10 p-3">
          <Loader2 className="h-6 w-6 animate-spin text-blue-400" />
        </div>

        <div className="flex-1">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="font-medium text-slate-100">
                Research agents are generating your report
              </p>
              <p className="mt-1 text-sm text-slate-400">
                This usually takes 2–3 minutes because the system searches
                multiple live sources before writing the final report.
              </p>
            </div>

            <div className="rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-sm text-slate-300">
              {formatElapsedTime(elapsedSeconds)}
            </div>
          </div>

          <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-800">
            <div className="h-full w-1/2 animate-pulse rounded-full bg-blue-500" />
          </div>

          <div className="mt-6 space-y-3">
            {steps.map((step, index) => {
              const Icon = step.icon;

              return (
                <div
                  key={step.label}
                  className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/60 p-3"
                >
                  <div className="rounded-lg border border-slate-700 bg-slate-950 p-2">
                    <Icon className="h-4 w-4 text-slate-300" />
                  </div>

                  <div className="flex-1">
                    <p className="text-sm text-slate-200">{step.label}</p>
                  </div>

                  <span className="text-xs text-slate-500">
                    Step {index + 1}
                  </span>
                </div>
              );
            })}
          </div>

          <p className="mt-5 text-xs leading-5 text-slate-500">
            Keep this tab open while the report is generated. First-time searches
            may take longer because results are collected from live web sources.
          </p>
        </div>
      </div>
    </div>
  );
}