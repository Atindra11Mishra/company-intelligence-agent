from typing import TypedDict, List, Dict, Any, Optional


class CompanyResearchState(TypedDict):
    company_input: str
    normalized_input: str
    display_name: str
    input_type: str

    sources: List[Dict[str, Any]]

    overview_sources: List[Dict[str, Any]]
    funding_sources: List[Dict[str, Any]]
    leadership_sources: List[Dict[str, Any]]
    competitor_sources: List[Dict[str, Any]]
    news_sources: List[Dict[str, Any]]
    hiring_sources: List[Dict[str, Any]]
    tech_stack_sources: List[Dict[str, Any]]

    overview_data: Optional[Dict[str, Any]]
    funding_data: Optional[Dict[str, Any]]
    leadership_data: Optional[Dict[str, Any]]
    competitor_data: Optional[Dict[str, Any]]
    news_data: Optional[Dict[str, Any]]
    hiring_data: Optional[Dict[str, Any]]
    tech_stack_data: Optional[Dict[str, Any]]

    synthesis: Optional[Dict[str, Any]]
    report_markdown: Optional[str]

    agent_trace: List[Dict[str, Any]]
    errors: List[str]