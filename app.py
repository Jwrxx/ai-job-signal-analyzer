import os
import json
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Create OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Job Signal Analyzer", page_icon="🧠", layout="centered")

st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #001233;  /* deep dark base */
    color: #979dac;
}

/* Card containers */
.card {
    background: #002855;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Section headers */
.section-title {
    font-size: 1.06rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: #e5e7eb;
}

/* Muted text */
.muted {
    color: #5c677d;
    font-size: 0.92rem;
}

/* Inputs */
textarea, input {
    background-color: #001845 !important;
    color: #e5e7eb !important;
    border-radius: 8px !important;
    border: 1px solid #33415c !important;
}

/* Buttons */
.stButton > button {
    background-color: #0466c8;
    color: white;
    border-radius: 8px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background-color: #0353a4;
}

/* Streamlit header (optional) */
header, footer {
    background-color: #001233 !important;
}
</style>
""", unsafe_allow_html=True)



st.title("🧠 AI Job Signal Analyzer")
st.caption("Paste a job description + your profile text. Get recruiter-grade signals, risks, and next steps.")

# Quick debug indicator (you can remove later)
key_loaded = bool(os.getenv("OPENAI_API_KEY"))


job_desc = st.text_area("Job Description", height=220, placeholder="Paste the job description here...")
profile = st.text_area("Your Profile (resume text or project summary)", height=220,
                       placeholder="Paste your resume text or a short summary of your skills/projects...")

run = st.button("Analyze Signals")

SYSTEM_PROMPT = """
You are a senior technical recruiter and hiring engineer.
Analyze candidate–job alignment using real hiring signals.

Rules:
- Do NOT rewrite resumes.
- No conversational tone.
- Focus on gaps, risks, seniority, and fast improvements.
- Output VALID JSON ONLY matching the schema.
"""

SCHEMA = {
    "fit_score_0_100": 0,
    "strength_signals": [],
    "missing_signals": [],
    "rejection_risks": [],
    "seniority_notes": "",
    "fastest_wins_7_days": [],
    "portfolio_upgrades_30_days": []
}

def analyze(job_text: str, profile_text: str) -> str:
    prompt = f"""
JOB DESCRIPTION:
{job_text}

CANDIDATE PROFILE:
{profile_text}

Return JSON ONLY using this schema (no extra keys):
{json.dumps(SCHEMA, indent=2)}
"""
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.output_text


if run:
    if not job_desc.strip() or not profile.strip():
        st.error("Please paste both the job description and your profile text.")
    elif not key_loaded:
        st.error("No API key found. Add OPENAI_API_KEY to your .env file and restart Streamlit.")
    else:
        with st.spinner("Analyzing hiring signals..."):
            raw = analyze(job_desc, profile)

        try:
            data = json.loads(raw)
            st.success("Done.")
            st.metric("Fit Score", f"{data.get('fit_score_0_100', 0)}/100")

            st.subheader("Strength Signals")
            st.write(data.get("strength_signals", []))

            st.subheader("Missing Signals")
            st.write(data.get("missing_signals", []))

            st.subheader("Rejection Risks")
            st.write(data.get("rejection_risks", []))

            st.subheader("Seniority Notes")
            st.write(data.get("seniority_notes", ""))

            st.subheader("Fastest Wins (7 days)")
            st.write(data.get("fastest_wins_7_days", []))

            st.subheader("Portfolio Upgrades (30 days)")
            st.write(data.get("portfolio_upgrades_30_days", []))

            st.download_button(
                "Download JSON report",
                data=json.dumps(data, indent=2),
                file_name="job_signal_report.json",
                mime="application/json"
            )

        except Exception:
            st.warning("AI returned non-JSON output. Showing raw output below:")
            st.code(raw)
