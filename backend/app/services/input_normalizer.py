import re
from urllib.parse import urlparse


def normalize_company_input(raw_input: str) -> dict:
    """
    Normalizes user input before research.
    Handles company names, website URLs, and LinkedIn company URLs.

    Returns:
    {
        "original_input": "...",
        "normalized_input": "...",
        "display_name": "...",
        "input_type": "company_name | website_url | linkedin_url"
    }
    """

    if not raw_input:
        return {
            "original_input": "",
            "normalized_input": "",
            "display_name": "",
            "input_type": "company_name"
        }

    cleaned = raw_input.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)

    lower_cleaned = cleaned.lower()

    if "linkedin.com/company/" in lower_cleaned:
        return normalize_linkedin_url(cleaned)

    if looks_like_url(cleaned):
        return normalize_website_url(cleaned)

    return normalize_company_name(cleaned)


def looks_like_url(value: str) -> bool:
    lower_value = value.lower()

    return (
        lower_value.startswith("http://")
        or lower_value.startswith("https://")
        or lower_value.startswith("www.")
        or "." in lower_value and " " not in lower_value
    )


def normalize_website_url(value: str) -> dict:
    original = value.strip()

    if not original.startswith(("http://", "https://")):
        url = "https://" + original
    else:
        url = original

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    normalized_url = f"https://{domain}"

    company_slug = domain.split(".")[0]
    display_name = slug_to_display_name(company_slug)

    return {
        "original_input": original,
        "normalized_input": normalized_url,
        "display_name": display_name,
        "input_type": "website_url"
    }


def normalize_linkedin_url(value: str) -> dict:
    original = value.strip()

    if not original.startswith(("http://", "https://")):
        url = "https://" + original
    else:
        url = original

    parsed = urlparse(url)
    path_parts = [part for part in parsed.path.split("/") if part]

    company_slug = ""

    if "company" in path_parts:
        company_index = path_parts.index("company")

        if company_index + 1 < len(path_parts):
            company_slug = path_parts[company_index + 1]

    display_name = slug_to_display_name(company_slug) if company_slug else original

    normalized_url = f"https://www.linkedin.com/company/{company_slug}" if company_slug else original

    return {
        "original_input": original,
        "normalized_input": normalized_url,
        "display_name": display_name,
        "input_type": "linkedin_url"
    }


def normalize_company_name(value: str) -> dict:
    cleaned = value.strip()
    cleaned = re.sub(r"\s+", " ", cleaned)

    display_name = smart_title_case(cleaned)

    return {
        "original_input": value,
        "normalized_input": display_name,
        "display_name": display_name,
        "input_type": "company_name"
    }


def slug_to_display_name(slug: str) -> str:
    slug = slug.strip().replace("-", " ").replace("_", " ")
    return smart_title_case(slug)


def smart_title_case(value: str) -> str:
    """
    Converts basic lowercase/uppercase inputs into cleaner display names.
    Keeps common abbreviations readable.
    """

    words = value.split(" ")

    special_cases = {
    "ai": "AI",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "github": "GitHub",
    "paypal": "PayPal",
    "youtube": "YouTube",
    "linkedin": "LinkedIn",
    "razorpay": "Razorpay",
    "stripe": "Stripe",
    "notion": "Notion",
    "perplexity": "Perplexity",
    "llc": "LLC",
    "inc": "Inc",
    "ltd": "Ltd",
    "pvt": "Pvt",
    "api": "API",
    "aws": "AWS",
    "ibm": "IBM",
    "hp": "HP",
    "tcs": "TCS",
    "hdfc": "HDFC",
    "icici": "ICICI"
}

    final_words = []

    for word in words:
        cleaned_word = word.strip()

        if not cleaned_word:
            continue

        lower_word = cleaned_word.lower()

        if lower_word in special_cases:
            final_words.append(special_cases[lower_word])
        else:
            final_words.append(lower_word.capitalize())

    return " ".join(final_words)