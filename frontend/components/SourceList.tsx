import { ExternalLink } from "lucide-react";
import type { Source } from "@/lib/types";

type SourceListProps = {
  sources: Source[];
};

export default function SourceList({ sources }: SourceListProps) {
  if (!sources.length) return null;

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-950 p-5">
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-100">Sources</h2>
          <p className="text-sm text-slate-400">
            URLs collected across specialist research agents.
          </p>
        </div>

        <span className="rounded-full border border-slate-700 bg-slate-900 px-3 py-1 text-xs text-slate-300">
          {sources.length} sources
        </span>
      </div>

      <div className="space-y-3">
        {sources.map((source, index) => (
          <a
            key={`${source.url}-${index}`}
            href={source.url}
            target="_blank"
            rel="noreferrer"
            className="block rounded-xl border border-slate-800 bg-slate-900/60 p-4 transition hover:border-blue-500/50 hover:bg-slate-900"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <h3 className="line-clamp-2 font-medium text-slate-100">
                  {source.title || "Untitled source"}
                </h3>

                <p className="mt-1 break-all text-xs text-blue-400">
                  {source.url}
                </p>

                {source.query && (
                  <p className="mt-2 text-xs text-slate-500">
                    Query: {source.query}
                  </p>
                )}
              </div>

              <ExternalLink className="h-4 w-4 shrink-0 text-slate-500" />
            </div>
          </a>
        ))}
      </div>
    </section>
  );
}