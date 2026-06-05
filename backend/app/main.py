from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.research_schema import ResearchRequest, ResearchResponse
from app.graph.workflow import company_research_graph


app = FastAPI(
    title="Company Intelligence Agent API",
    description="Autonomous company research API using LangGraph, Tavily, and Groq.",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "Company Intelligence Agent API is running"
    }


@app.post("/research", response_model=ResearchResponse)
def research_company(request: ResearchRequest):
    try:
        initial_state = {
    "company_input": request.company_input,
    "normalized_input": "",
    "display_name": "",
    "input_type": "",

    "sources": [],

    "overview_sources": [],
    "funding_sources": [],
    "leadership_sources": [],
    "competitor_sources": [],
    "news_sources": [],
    "hiring_sources": [],
    "tech_stack_sources": [],

    "overview_data": None,
    "funding_data": None,
    "leadership_data": None,
    "competitor_data": None,
    "news_data": None,
    "hiring_data": None,
    "tech_stack_data": None,

    "synthesis": None,
    "report_markdown": None,

    "agent_trace": [],
    "errors": []
}

        final_state = company_research_graph.invoke(initial_state)

        if final_state.get("errors"):
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Research workflow failed.",
                    "errors": final_state["errors"]
                }
            )

        return {
    "company_input": final_state["display_name"],
    "report_markdown": final_state["report_markdown"],
    "sources": final_state["sources"],
    "agent_trace": final_state["agent_trace"]
}

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(error)}"
        )