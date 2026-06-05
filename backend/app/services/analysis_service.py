import json
from typing import List, Dict, Any
from app.services.groq_service import generate_with_groq


def analyze_section(
    company_input: str,
    sources: List[Dict[str, Any]],
    section_name: str,
    instruction: str
) -> Dict[str, Any]:
    """
    Generic section analyzer.
    Takes all sources but asks the LLM to extract only one focused section.
    """

    source_text = format_sources_for_prompt(sources)

    prompt = f"""
You are a company intelligence analyst.

Company:
{company_input}

Research section:
{section_name}

Your task:
{instruction}

Available sources:
{source_text}

Return ONLY valid JSON. Do not include markdown. Do not include explanation outside JSON.

Use this JSON structure:

{{
  "section": "{section_name}",
  "summary": "",
  "key_findings": [],
  "confidence": "High | Medium | Low",
  "confidence_reason": "",
  "source_urls": []
}}

Rules:
- Do not invent facts.
- If information is not clearly available, say so.
- Use only the provided sources.
- Keep findings concise.
"""

    raw_output = generate_with_groq(prompt)

    return safe_json_parse(raw_output, section_name)


def synthesize_sections(
    company_input: str,
    overview_data: Dict[str, Any],
    funding_data: Dict[str, Any],
    leadership_data: Dict[str, Any],
    competitor_data: Dict[str, Any],
    news_data: Dict[str, Any],
    hiring_data: Dict[str, Any],
    tech_stack_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Merges all section-level outputs into one synthesized intelligence object.
    """

    prompt = f"""
You are a senior business intelligence analyst.

Company:
{company_input}

You are given section-level research outputs.

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

Create a synthesized JSON object.

Return ONLY valid JSON. Do not include markdown.

Use this JSON structure:

{{
  "company": "{company_input}",
  "executive_summary": "",
  "strongest_findings": [],
  "weak_or_missing_areas": [],
  "possible_conflicts": [],
  "overall_confidence": "High | Medium | Low"
}}

Rules:
- Deduplicate repeated findings.
- Mention missing areas.
- Mention conflicts if any.
- Do not invent facts.
"""

    raw_output = generate_with_groq(prompt)

    return safe_json_parse(raw_output, "synthesis")


def format_sources_for_prompt(sources: List[Dict[str, Any]]) -> str:
    """
    Keeps source formatting compact to reduce token load.
    """

    formatted = []

    for index, source in enumerate(sources, start=1):
        formatted.append(
            f"""
Source {index}
Title: {source.get("title")}
URL: {source.get("url")}
Snippet: {source.get("content")}
"""
        )

    return "\n".join(formatted)


def safe_json_parse(raw_output: str, section_name: str) -> Dict[str, Any]:
    """
    Attempts to parse LLM JSON safely.
    If parsing fails, returns fallback object.
    """

    try:
        cleaned = raw_output.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned.replace("```", "").strip()

        return json.loads(cleaned)

    except Exception:
        return {
            "section": section_name,
            "summary": raw_output,
            "key_findings": [],
            "confidence": "Low",
            "confidence_reason": "Model returned non-JSON output.",
            "source_urls": []
        }