# Company Intelligence Agent

A LangGraph-powered company research agent that generates structured company intelligence reports from a company name, website URL, or LinkedIn company link.

The system researches public web signals such as company overview, funding, leadership, competitors, recent news, hiring trends, and tech stack signals, then generates a clean markdown intelligence report with sources and an agent execution trace.

---

## Screenshots

### Landing Page

> Add your first screenshot here

```md
![Company Intelligence Agent Landing Page](./frontend/public/Screenshot%202026-06-05%20175017.png)
```

### Generated Intelligence Report

> Add your second screenshot here

```md
![Generated Company Intelligence Report](./frontend/public/Screenshot%202026-06-05%20175028.png)
```

---

## What This Project Does

The user enters a company name or URL, for example:

```txt
Stripe
```

or

```txt
https://stripe.com
```

or

```txt
https://www.linkedin.com/company/stripe
```

The application then generates a structured company intelligence report containing:

* Company overview
* Funding, valuation, and revenue signals
* Leadership team
* Competitors and market position
* Recent news and announcements
* Hiring trends
* Tech stack signals
* Confidence assessment
* Source list
* LangGraph agent trace

---

## Why This Project Is Useful

This project is designed for fast company research and public-web due diligence.

Possible use cases:

* Sales teams researching prospects before outreach
* Job seekers researching companies before interviews
* Recruiters understanding company hiring signals
* Investors performing quick preliminary company research
* Founders studying competitors and market positioning
* Developers demonstrating production-style agent workflows

---

## Key Features

### 1. Multi-Step LangGraph Workflow

The backend uses LangGraph to coordinate multiple research steps:

```txt
Input Normalizer
      ↓
Overview Research
      ↓
Funding Research
      ↓
Leadership Research
      ↓
Competitor Research
      ↓
News Research
      ↓
Hiring Research
      ↓
Tech Stack Research
      ↓
Source Deduplication
      ↓
Report Generator
```

Each node has a focused responsibility, making the workflow easier to debug, extend, and monitor.

---

### 2. Company Input Normalization

The backend cleans user input before research.

Examples:

```txt
"   stripe   "      → Stripe
"STRIPE"            → Stripe
"https://stripe.com" → Stripe
"www.notion.so"     → Notion
```

This improves the final report title, search quality, and user experience.

---

### 3. Section-Specific Research

Instead of running one generic search, the system performs targeted searches for each report section.

Examples:

* Funding queries search for valuation, revenue, investors, funding rounds
* Hiring queries search for careers pages, engineering roles, AI roles, product roles
* Tech stack queries search for engineering blogs, backend jobs, infrastructure roles, and developer signals
* News queries search for recent announcements, partnerships, launches, and updates

This gives better results than a basic scraper or simple LLM prompt.

---

### 4. Hiring Trend Analysis

The agent searches job postings and hiring signals to infer what the company may be investing in.

Example insights:

* Hiring multiple ML engineers may indicate AI infrastructure investment
* Infrastructure and platform roles may indicate scaling work
* Enterprise sales roles may indicate go-to-market expansion
* Product roles around developer tools may indicate platform investment

---

### 5. Tech Stack Signal Extraction

The system infers technology usage from public job posts, engineering blogs, and source snippets.

Example signals may include:

* Programming languages
* Cloud platforms
* Databases
* Infrastructure tools
* Data engineering tools
* AI/ML tooling

The report marks these as inferred unless directly confirmed by a strong source.

---

### 6. Agent Trace UI

The frontend displays the completed research workflow as an agent trace.

Example:

```txt
✓ Input Normalizer completed
✓ Overview sources collected
✓ Funding and valuation sources collected
✓ Leadership sources collected
✓ Hiring trend sources collected
✓ Tech stack signal sources collected
✓ Sources deduplicated
✓ Final markdown report generated
```

This makes the project more transparent and gives users confidence that the report was built through a structured process.

---

### 7. Recruiter-Friendly Frontend

The frontend includes:

* Clean landing section
* Company input form
* Long-running loading state with timer
* Agent trace timeline
* Markdown report viewer
* Source list
* Responsive dark UI

The loading state clearly tells users that report generation can take around 2–3 minutes because the system searches multiple live public sources.

---

## Current Status

This is a working MVP.

Currently implemented:

* FastAPI backend
* LangGraph research workflow
* Tavily-powered web search
* Groq LLM report generation
* Lean one-call report generation mode
* Company input normalization
* Agent trace response
* Next.js frontend
* Markdown report rendering
* Source list rendering
* User-friendly loading state

Planned improvements:

* Source quality scoring
* Tavily Extract integration
* Firecrawl support for official website crawling
* Supabase caching
* Report history
* PDF export
* Real-time streaming agent progress
* Advanced deep-research mode
* Section-level confidence scoring based on source quality

---

## Tech Stack

### Frontend

* Next.js
* TypeScript
* Tailwind CSS
* React Markdown
* Lucide Icons

### Backend

* Python
* FastAPI
* LangGraph
* Tavily Search API
* Groq LLM API
* Pydantic
* Uvicorn

### Planned

* Supabase Postgres for caching and saved reports
* Firecrawl for official website crawling
* Tavily Extract API for deeper page extraction
* Vercel for frontend deployment
* Render/Railway for backend deployment

---

## Architecture

```txt
User Input
   ↓
Next.js Frontend
   ↓
FastAPI Backend
   ↓
LangGraph Workflow
   ↓
Specialist Research Nodes
   ├── Overview Research
   ├── Funding Research
   ├── Leadership Research
   ├── Competitor Research
   ├── News Research
   ├── Hiring Research
   └── Tech Stack Research
   ↓
Source Deduplication
   ↓
Groq LLM Report Generator
   ↓
Markdown Report + Sources + Agent Trace
   ↓
Frontend Report Viewer
```

---

## Backend Workflow

The backend uses a lean MVP workflow to reduce LLM cost and avoid free-tier rate limits.

Instead of making one LLM call per section, the current version performs multiple search steps and then uses a single LLM call to generate the final report.

```txt
Multiple research/search nodes
        ↓
Deduplicated sources
        ↓
Single final report generation call
```

This keeps the project practical for free-tier usage while still preserving the LangGraph multi-step architecture.

---

## API Endpoint

### `POST /research`

Request body:

```json
{
  "company_input": "Stripe"
}
```

Response body:

```json
{
  "company_input": "Stripe",
  "report_markdown": "# Company Intelligence Report: Stripe...",
  "sources": [
    {
      "query": "Stripe funding valuation revenue investors",
      "title": "Stripe valuation jumps...",
      "url": "https://example.com",
      "content": "Source snippet...",
      "score": 0.94
    }
  ],
  "agent_trace": [
    {
      "agent": "overview",
      "status": "completed",
      "sources_found": 5,
      "message": "Company overview sources collected"
    }
  ]
}
```

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/company-intelligence-agent.git
cd company-intelligence-agent
```

---

## Backend Setup

### 2. Move into Backend

```bash
cd backend
```

### 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

#### Windows PowerShell

```bash
venv\Scripts\Activate.ps1
```

#### Windows Git Bash

```bash
source venv/Scripts/activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create `.env`

Create a `.env` file inside the `backend` folder:

```env
TAVILY_API_KEY=your_tavily_api_key
GROQ_API_KEY=your_groq_api_key
```

### 6. Run Backend Server

```bash
py -m uvicorn app.main:app --reload
```

Backend runs on:

```txt
http://127.0.0.1:8000
```

Swagger docs:

```txt
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

### 7. Move into Frontend

Open a second terminal:

```bash
cd frontend
```

### 8. Install Dependencies

```bash
npm install
```

### 9. Create `.env.local`

Create a `.env.local` file inside the `frontend` folder:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### 10. Run Frontend

```bash
npm run dev
```

Frontend runs on:

```txt
http://localhost:3000
```

---

## Example Companies to Test

Try:

```txt
Stripe
OpenAI
Notion
Razorpay
Perplexity AI
Anthropic
Shopify
Airbnb
```

The system works best for companies with public web signals such as websites, news coverage, job postings, leadership pages, or funding data.

---

## Limitations

The current version depends on publicly available information.

It works best for:

* Startups
* SaaS companies
* Fintech companies
* AI companies
* VC-backed companies
* Publicly visible businesses
* Companies with active job posts or news coverage

It may produce weaker reports for:

* Very small local businesses
* Stealth startups
* Companies with no website
* Companies with little public data
* Companies with blocked or unavailable pages

When data is missing, the report is designed to say that information is not clearly available instead of hallucinating.

---

## Free-Tier Considerations

The project currently uses Tavily and Groq APIs.

To make the MVP practical on free tiers, the backend uses a lean report-generation mode:

* Multiple search calls
* One final LLM call
* No section-level LLM calls
* No deep extraction by default

This reduces cost and avoids excessive token usage.

---

## Future Improvements

### Short-Term

* Deploy frontend on Vercel
* Deploy backend on Render or Railway
* Add GitHub README screenshots
* Add project demo video
* Add portfolio card

### Product Improvements

* Add PDF export
* Add source quality scoring
* Add report history
* Add Supabase caching
* Add copy-to-clipboard for markdown
* Add download report button
* Add company type selector

### Agent Improvements

* Add Tavily Extract for top URLs
* Add Firecrawl for official website crawling
* Add conditional routing
* Add deep report mode
* Add real-time streaming progress
* Add confidence scoring based on source quality
* Add conflict detection between sources

---

## Resume Bullet

```txt
Built a full-stack Company Intelligence Agent using FastAPI, LangGraph, Next.js, Tavily, and Groq that researches public web signals and generates structured company reports with funding, leadership, competitors, hiring trends, tech stack signals, sources, and agent execution trace.
```

Alternative stronger version:

```txt
Built an autonomous Company Intelligence Agent with LangGraph-based research workflow, FastAPI backend, and Next.js frontend, generating source-backed company intelligence reports from a company name or URL with agent trace, hiring trend analysis, tech stack inference, and confidence-aware reporting.
```

---

## Project Positioning

This project is not just a company scraper.

It demonstrates:

* Agent workflow design
* LangGraph orchestration
* FastAPI backend engineering
* LLM-based report generation
* Public web intelligence collection
* Frontend product design
* API integration
* Source-backed AI output
* Practical free-tier optimization

The current version is designed as a live MVP, with deeper intelligence and production optimizations planned after deployment.
