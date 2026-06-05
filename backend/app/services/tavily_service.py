import requests
from typing import List, Dict, Any
from app.config import TAVILY_API_KEY


TAVILY_SEARCH_URL = "https://api.tavily.com/search"


def run_tavily_search(
    queries: List[str],
    max_results_per_query: int = 2,
    total_limit: int = 8
) -> List[Dict[str, Any]]:
    """
    Generic Tavily search runner.
    Used by section-specific research nodes.
    """

    all_results = []

    for query in queries:
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "include_raw_content": False,
            "max_results": max_results_per_query
        }

        response = requests.post(TAVILY_SEARCH_URL, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        for item in results:
            all_results.append({
                "query": query,
                "title": item.get("title"),
                "url": item.get("url"),
                "content": trim_text(item.get("content"), max_chars=900),
                "score": item.get("score")
            })

    unique_results = deduplicate_sources(all_results)

    return unique_results[:total_limit]


def search_overview_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} company overview founding headquarters business model",
        f"{company_input} about company founders headquarters products",
        f"{company_input} company profile industry business model"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=6)


def search_funding_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} funding valuation revenue investors",
        f"{company_input} latest valuation funding round investors",
        f"{company_input} annual revenue estimate payment volume"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=6)


def search_leadership_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} founders CEO leadership team executives",
        f"{company_input} management team c-suite board members",
        f"{company_input} recent leadership hires executive changes"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=6)


def search_competitor_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} competitors market position alternatives",
        f"{company_input} competitive landscape market share",
        f"{company_input} vs competitors industry analysis"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=6)


def search_news_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} latest news last 30 days",
        f"{company_input} recent announcements partnerships acquisition launch",
        f"{company_input} newsroom latest updates"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=6)


def search_hiring_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} careers jobs hiring engineering product roles",
        f"{company_input} open jobs software engineer machine learning data",
        f"{company_input} careers infrastructure product manager AI jobs",
        f"site:greenhouse.io {company_input} jobs engineering",
        f"site:lever.co {company_input} jobs engineering",
        f"site:ashbyhq.com {company_input} jobs engineering"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=8)


def search_tech_stack_sources(company_input: str) -> List[Dict[str, Any]]:
    queries = [
        f"{company_input} engineering blog tech stack architecture",
        f"{company_input} software engineer job Python Go Java Kubernetes AWS",
        f"{company_input} backend engineer job description tech stack",
        f"{company_input} infrastructure engineer job Kubernetes Terraform",
        f"{company_input} data engineer job Kafka Spark Airflow",
        f"{company_input} machine learning engineer job PyTorch Python"
    ]

    return run_tavily_search(queries, max_results_per_query=2, total_limit=8)


def search_company_intelligence(company_input: str) -> List[Dict[str, Any]]:
    """
    Backward-compatible generic search.
    Useful for testing or fallback.
    """

    all_sources = []

    all_sources.extend(search_overview_sources(company_input))
    all_sources.extend(search_funding_sources(company_input))
    all_sources.extend(search_leadership_sources(company_input))
    all_sources.extend(search_competitor_sources(company_input))
    all_sources.extend(search_news_sources(company_input))

    unique_results = deduplicate_sources(all_sources)

    return unique_results[:10]


def deduplicate_sources(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen_urls = set()
    unique_results = []

    for item in results:
        url = item.get("url")

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_results.append(item)

    return unique_results


def trim_text(text: str | None, max_chars: int = 900) -> str:
    if not text:
        return ""

    text = text.strip()

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "..."