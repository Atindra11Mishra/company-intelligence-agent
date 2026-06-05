import json
from typing import Dict, Any, List
from app.services.groq_service import generate_with_groq

def build_lean_company_report(
    company_input: str,
    sources: List[Dict[str, Any]]
) -> str:
    """
    Lean MVP report generator.
    Uses one LLM call only.
    Best for free-tier deployment.
    """

    compact_sources = format_sources_for_lean_report(sources)

    prompt = f"""
You are a senior company intelligence analyst.

Company:
{company_input}

You are given source snippets collected from multiple research agents:
{compact_sources}

Create a structured markdown company intelligence report.

Use this exact structure:

# Company Intelligence Report: {company_input}

## Executive Summary

## 1. Company Overview
Include founding year, HQ, business model, products/services, industry, and size if available.

## 2. Funding, Valuation, and Revenue
Include funding, valuation, investors, revenue estimates, transaction volume, or scale metrics if available.
Clearly label estimates.

## 3. Leadership Team
Include founders, CEO, C-suite, board members, and notable recent hires if available.

## 4. Competitors and Market Position
Include direct competitors, indirect competitors, market position, differentiation, and market share if available.

## 5. Recent News
Include recent launches, partnerships, acquisitions, funding, product announcements, or regulatory updates.

## 6. Hiring Trends
Infer what the company may be investing in from job posts and hiring signals.
Mention if hiring data is weak.

## 7. Tech Stack Signals
Infer stack only from job posts, engineering blogs, official pages, or credible source snippets.
Do not guess. Mark all tech stack information as inferred unless directly confirmed.

## 8. Confidence Assessment
Give confidence for each section:
- High
- Medium
- Low

Explain briefly why.

## 9. Sources
List the most useful source titles and URLs.

Rules:
- Do not invent facts.
- If something is missing, say "Not clearly available from retrieved sources."
- Prefer official company pages, credible financial/news sources, and direct job posts.
- Be concise but useful.
"""

    return generate_with_groq(prompt)


def format_sources_for_lean_report(sources: List[Dict[str, Any]]) -> str:
    """
    Formats only compact source data to reduce token usage.
    """

    formatted = []

    for index, source in enumerate(sources[:24], start=1):
        formatted.append(
            f"""
Source {index}
Query: {source.get("query")}
Title: {source.get("title")}
URL: {source.get("url")}
Snippet: {str(source.get("content", ""))[:650]}
"""
        )

    return "\n".join(formatted)

def build_company_report_from_sections(
    company_input: str,
    overview_data: Dict[str, Any],
    funding_data: Dict[str, Any],
    leadership_data: Dict[str, Any],
    competitor_data: Dict[str, Any],
    news_data: Dict[str, Any],
    hiring_data: Dict[str, Any],
    tech_stack_data: Dict[str, Any],
    synthesis: Dict[str, Any],
    sources: List[Dict[str, Any]]
) -> str:
    """
    Builds the final markdown report from structured section outputs.
    """

    prompt = f"""
You are creating a polished company intelligence report in markdown.

Company:
{company_input}

Synthesis:
{json.dumps(synthesis, indent=2)}

Overview:
{json.dumps(overview_data, indent=2)}

Funding:
{json.dumps(funding_data, indent=2)}

Leadership:
{json.dumps(leadership_data, indent=2)}

Competitors:
{json.dumps(competitor_data, indent=2)}

News:
{json.dumps(news_data, indent=2)}

Hiring:
{json.dumps(hiring_data, indent=2)}

Tech Stack:
{json.dumps(tech_stack_data, indent=2)}

Sources:
{format_sources_for_report(sources)}

Create a structured markdown report with these sections:

# Company Intelligence Report: {company_input}

## Executive Summary

## 1. Company Overview

## 2. Funding, Valuation, and Revenue

## 3. Leadership Team

## 4. Competitors and Market Position

## 5. Recent News

## 6. Hiring Trends

## 7. Tech Stack Signals

## 8. Confidence Assessment

## 9. Sources

Rules:
- Be concise but useful.
- Do not invent facts.
- Clearly say when information is unavailable.
- For inferred tech stack or hiring trends, explicitly say "inferred".
- Include confidence labels.
"""

    return generate_with_groq(prompt)


def format_sources_for_report(sources: List[Dict[str, Any]]) -> str:
    formatted = []

    for index, source in enumerate(sources, start=1):
        formatted.append(
            f"{index}. {source.get('title')} - {source.get('url')}"
        )

    return "\n".join(formatted)