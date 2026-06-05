from langgraph.graph import StateGraph, END
from app.services.input_normalizer import normalize_company_input
from app.graph.state import CompanyResearchState

from app.services.tavily_service import (
    deduplicate_sources,
    search_overview_sources,
    search_funding_sources,
    search_leadership_sources,
    search_competitor_sources,
    search_news_sources,
    search_hiring_sources,
    search_tech_stack_sources,
)

from app.services.report_service import build_lean_company_report

def normalize_input_node(state: CompanyResearchState) -> CompanyResearchState:
    normalized = normalize_company_input(state["company_input"])

    return {
        **state,
        "normalized_input": normalized["normalized_input"],
        "display_name": normalized["display_name"],
        "input_type": normalized["input_type"],
        "agent_trace": add_trace(
            state,
            agent="input_normalizer",
            status="completed",
            message=f"Input normalized to {normalized['display_name']}"
        )
    }

def add_trace(
    state: CompanyResearchState,
    agent: str,
    status: str,
    sources_found: int = 0,
    confidence: str | None = None,
    message: str | None = None
) -> list:
    trace = state.get("agent_trace", [])

    trace_item = {
        "agent": agent,
        "status": status,
        "sources_found": sources_found
    }

    if confidence:
        trace_item["confidence"] = confidence

    if message:
        trace_item["message"] = message

    return trace + [trace_item]


def overview_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_overview_sources(state["normalized_input"])

    return {
        **state,
        "overview_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="overview",
            status="completed",
            sources_found=len(sources),
            message="Company overview sources collected"
        )
    }


def funding_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_funding_sources(state["normalized_input"])

    return {
        **state,
        "funding_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="funding",
            status="completed",
            sources_found=len(sources),
            message="Funding and valuation sources collected"
        )
    }


def leadership_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_leadership_sources(state["normalized_input"])

    return {
        **state,
        "leadership_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="leadership",
            status="completed",
            sources_found=len(sources),
            message="Leadership sources collected"
        )
    }


def competitor_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_competitor_sources(state["normalized_input"])

    return {
        **state,
        "competitor_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="competitors",
            status="completed",
            sources_found=len(sources),
            message="Competitor and market sources collected"
        )
    }


def news_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_news_sources(state["normalized_input"])

    return {
        **state,
        "news_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="news",
            status="completed",
            sources_found=len(sources),
            message="Recent news sources collected"
        )
    }


def hiring_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_hiring_sources(state["normalized_input"])

    return {
        **state,
        "hiring_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="hiring",
            status="completed",
            sources_found=len(sources),
            message="Hiring trend sources collected"
        )
    }


def tech_stack_node(state: CompanyResearchState) -> CompanyResearchState:
    sources = search_tech_stack_sources(state["normalized_input"])

    return {
        **state,
        "tech_stack_sources": sources,
        "agent_trace": add_trace(
            state,
            agent="tech_stack",
            status="completed",
            sources_found=len(sources),
            message="Tech stack signal sources collected"
        )
    }


def collect_sources_node(state: CompanyResearchState) -> CompanyResearchState:
    all_sources = []

    all_sources.extend(state.get("overview_sources", []))
    all_sources.extend(state.get("funding_sources", []))
    all_sources.extend(state.get("leadership_sources", []))
    all_sources.extend(state.get("competitor_sources", []))
    all_sources.extend(state.get("news_sources", []))
    all_sources.extend(state.get("hiring_sources", []))
    all_sources.extend(state.get("tech_stack_sources", []))

    unique_sources = deduplicate_sources(all_sources)

    return {
        **state,
        "sources": unique_sources,
        "agent_trace": add_trace(
            state,
            agent="collect_sources",
            status="completed",
            sources_found=len(unique_sources),
            message="All sources deduplicated"
        )
    }


def generate_report_node(state: CompanyResearchState) -> CompanyResearchState:
    try:
        report_markdown = build_lean_company_report(
            company_input=state["display_name"],
            sources=state.get("sources", [])
        )

        return {
            **state,
            "report_markdown": report_markdown,
            "errors": state.get("errors", []),
            "agent_trace": add_trace(
                state,
                agent="report_generator",
                status="completed",
                message="Final markdown report generated using lean one-call mode"
            )
        }

    except Exception as error:
        return {
            **state,
            "report_markdown": None,
            "errors": state.get("errors", []) + [f"generate_report_node failed: {str(error)}"],
            "agent_trace": add_trace(
                state,
                agent="report_generator",
                status="failed",
                message=str(error)
            )
        }


def build_company_research_graph():
    graph = StateGraph(CompanyResearchState)
    
    
    graph.add_node("overview", overview_node)
    graph.add_node("normalize_input", normalize_input_node)
    graph.add_node("funding", funding_node)
    graph.add_node("leadership", leadership_node)
    graph.add_node("competitors", competitor_node)
    graph.add_node("news", news_node)
    graph.add_node("hiring", hiring_node)
    graph.add_node("tech_stack", tech_stack_node)
    graph.add_node("collect_sources", collect_sources_node)
    graph.add_node("generate_report", generate_report_node)

    graph.set_entry_point("normalize_input")

    graph.add_edge("normalize_input", "overview")
    graph.add_edge("overview", "funding")
    graph.add_edge("funding", "leadership")
    graph.add_edge("leadership", "competitors")
    graph.add_edge("competitors", "news")
    graph.add_edge("news", "hiring")
    graph.add_edge("hiring", "tech_stack")
    graph.add_edge("tech_stack", "collect_sources")
    graph.add_edge("collect_sources", "generate_report")
    graph.add_edge("generate_report", END)

    return graph.compile()


company_research_graph = build_company_research_graph()