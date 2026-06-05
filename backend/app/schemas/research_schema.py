from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class ResearchRequest(BaseModel):
    company_input: str


class SourceItem(BaseModel):
    title: str
    url: str
    content: Optional[str] = None


class ResearchResponse(BaseModel):
    company_input: str
    report_markdown: str
    sources: List[Dict[str, Any]]
    agent_trace: List[Dict[str, Any]]