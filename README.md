# AI Job Signal Analyzer

A Python-based AI tool that analyzes recruiter and hiring signals by comparing job descriptions against candidate profiles.  
Instead of rewriting resumes, it surfaces **fit score, missing signals, rejection risks, and actionable technical improvements**.

## Why This Project
Most candidates don’t know *why* they’re getting rejected.  
This tool reverse-engineers recruiter decision-making using AI to highlight:
- Skill gaps
- Seniority mismatches
- High-signal improvements that matter to hiring teams

## Features
- Fit score (0–100)
- Strength signals vs missing signals
- Rejection risks and seniority notes
- Fastest wins (7 days) and portfolio upgrades (30 days)
- Downloadable structured JSON report

## Tech Stack
- Python
- Streamlit
- OpenAI API
- python-dotenv

## How It Works
1. Paste a job description
2. Paste a candidate profile or resume text
3. AI analyzes recruiter-level hiring signals
4. Results are returned as structured insights

## Setup & Run
```bash
python -m pip install streamlit openai python-dotenv
