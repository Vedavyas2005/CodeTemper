## CodeTemper: Judgment without ego.

CodeTemper is a calm, senior-style code review assistant that focuses on clarity, trade-offs, and long-term maintainability rather than surface-level correctness.

It is designed to help developers think like experienced reviewers before opening a pull request.

## Live Deployment at: https://codetemper-xckv6c6nnyhnxrxasninxu.streamlit.app/

## Demo At: 

## ✨ Why CodeTemper Exists

Modern code review often fails for reasons that tools don’t address:

Feedback is vague (“this feels complex”)

Reviewers focus on style, not design

Trade-offs remain implicit

Junior engineers don’t know what questions reviewers will ask

CodeTemper exists to surface engineering judgment early, so human code reviews become faster, calmer, and more productive.

This tool does not replace code review.
It improves the quality of conversations around code.

## 🧠 What CodeTemper Reviews (and What It Doesn’t)
# ✅ Focuses on

Cognitive load (how hard the code is to reason about)

Over-engineering and premature abstraction

Readability and naming clarity

Future breakage risk (6–12 month horizon)

Design trade-offs

Senior-style PR feedback

# ❌ Explicitly does NOT

Execute code

Prove correctness

Auto-refactor

Enforce style rules

This restraint is intentional.

## 🧩 Core Features
# 1️⃣ Cognitive Load Score

Estimates the mental effort required to understand the code under pressure.

“Correct but difficult to reason about during incidents.”

# 2️⃣ Over-Engineering Detection

Identifies abstractions that add complexity without clear present benefit.

“This abstraction saves lines but increases mental overhead.”

# 3️⃣ Future Breakage Analysis

Simulates likely changes over the next 6–12 months and highlights brittle areas.

# 4️⃣ Readability & Clarity Review

Flags unclear naming, deep nesting, and implicit assumptions.

# 5️⃣ “What Not to Change”

Highlights good decisions worth preserving — an often-missing part of reviews.

# 6️⃣ Senior Review Summary

A short PR-style summary written in the voice of a calm, experienced engineer.

## 🖥️ How It’s Used

Paste code or a PR diff

Click “Review calmly 🌸”

Receive structured, human-readable feedback

Refine before opening a pull request

Typical use time: 2–3 minutes

## 🛠️ Tech Stack

Frontend / UI: Streamlit

Backend: Python 3.13

AI Model: Google Gemini (structured JSON output)

Validation: Pydantic v2

Deployment: Streamlit Cloud / Render / Railway

## 🧪 Reliability & Engineering Decisions

Uses strict JSON schema validation

Includes self-repair retry for malformed LLM outputs

Avoids over-automation to preserve human judgment

Designed with editor correctness (Pylance-safe typing)

These decisions reflect real-world GenAI production constraints.

## 🚀 Getting Started
1. Local Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
2. Add your API key:
```bash
# .streamlit/secrets.toml
GEMINI_API_KEY="your_api_key_here"
```

3. Run the app:

streamlit run app.py

## 🌱 Design Philosophy

Good code is not code that is clever.
It is code that is easy to reason about when things go wrong.

CodeTemper is intentionally:

Calm

Minimal

Honest

Slightly conservative

Because that’s how real engineering teams operate.

## ⚠️ Limitations (By Design)

Does not replace human reviewers

Does not catch runtime bugs

Output depends on input context

Focuses on judgment, not enforcement

Acknowledging these limitations is part of responsible AI usage.

## 👤 Author
Built by Vedavyas Dasari
Focused on AI systems that respect human cognition, judgment, and mental well-being.

## Main Goal in a single Line:
CodeTemper is an AI-assisted code review tool that makes engineering trade-offs explicit before human review.

Built by Vedavyas Dasari
Focused on AI systems that respect human cognition, judgment, and mental well-being.
