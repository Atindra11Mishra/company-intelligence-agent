export type Source = {
  query?: string;
  title: string;
  url: string;
  content?: string;
  score?: number;
};

export type AgentTraceItem = {
  agent: string;
  status: string;
  sources_found?: number;
  confidence?: "High" | "Medium" | "Low" | string;
  message?: string;
};

export type ResearchResponse = {
  company_input: string;
  report_markdown: string;
  sources: Source[];
  agent_trace: AgentTraceItem[];
};

export type ResearchRequest = {
  company_input: string;
};