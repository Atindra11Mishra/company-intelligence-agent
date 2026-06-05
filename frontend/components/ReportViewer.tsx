import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type ReportViewerProps = {
  markdown: string;
};

export default function ReportViewer({ markdown }: ReportViewerProps) {
  if (!markdown) return null;

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-950 p-5">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-100">
          Intelligence Report
        </h2>
        <p className="text-sm text-slate-400">
          Structured markdown report generated from researched sources.
        </p>
      </div>

      <article className="prose prose-invert max-w-none prose-headings:scroll-mt-24 prose-h1:text-2xl prose-h2:border-b prose-h2:border-slate-800 prose-h2:pb-2 prose-p:text-slate-300 prose-li:text-slate-300 prose-strong:text-slate-100 prose-a:text-blue-400">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
      </article>
    </section>
  );
}