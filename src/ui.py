from __future__ import annotations

import streamlit as st
from src.review_schema import CodeReviewReport, Finding


def inject_soft_sakura_css() -> None:
    st.markdown(
        """
        <style>
          /* Soft sakura wash without being loud */
          .stApp {
            background:
              radial-gradient(circle at 10% 10%, rgba(255, 182, 193, 0.25), transparent 35%),
              radial-gradient(circle at 90% 15%, rgba(255, 105, 180, 0.10), transparent 40%),
              radial-gradient(circle at 30% 85%, rgba(255, 228, 236, 0.60), transparent 45%),
              #FFF7FA;
          }

          /* Subtle card styling */
          div[data-testid="stExpander"] > details {
            border-radius: 14px;
            border: 1px solid rgba(210, 4, 45, 0.18);
            background: rgba(255, 255, 255, 0.7);
          }

          /* Buttons */
          .stButton button {
            border-radius: 12px;
            border: 1px solid rgba(210, 4, 45, 0.35);
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def severity_badge(sev: str) -> str:
    if sev == "high":
        return "🔴 high"
    if sev == "medium":
        return "🟠 medium"
    return "🟢 low"


def render_finding(f: Finding) -> None:
    st.markdown(f"**{f.title}** — {severity_badge(f.severity)}")
    st.write(f.explanation)
    st.markdown("**Consider:**")
    st.write(f.suggestion)


def render_report(report: CodeReviewReport) -> None:
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Cognitive Load", f"{report.cognitive_load_score} / 10")
        st.caption(report.cognitive_load_reason)

    with c2:
        st.metric("PR Risk", report.pr_risk.upper())
        st.caption(report.pr_risk_reason)

    with st.expander("Senior review summary", expanded=True):
        st.write(report.senior_review_summary)

    with st.expander("What not to change"):
        if report.what_not_to_change:
            for item in report.what_not_to_change:
                st.write(f"• {item}")
        else:
            st.write("Nothing specific to preserve was identified — but that can also mean the code is still forming.")

    with st.expander("Readability"):
        if report.readability_issues:
            for f in report.readability_issues:
                render_finding(f)
                st.divider()
        else:
            st.write("No major readability concerns detected.")

    with st.expander("Over-engineering"):
        if report.overengineering_flags:
            for f in report.overengineering_flags:
                render_finding(f)
                st.divider()
        else:
            st.write("No clear signs of premature abstraction were detected.")

    with st.expander("Future breakage (6–12 months)"):
        if report.future_breakage_risks:
            for f in report.future_breakage_risks:
                render_finding(f)
                st.divider()
        else:
            st.write("No clear brittleness patterns detected for likely future changes.")
