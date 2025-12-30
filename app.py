from __future__ import annotations

import os
import streamlit as st

from src.gemini_client import build_client
from src.reviewer import review_code
from src.ui import inject_soft_sakura_css, render_report


APP_TITLE = "Engineering Judgment Review"
APP_SUBTITLE = "Thoughtful feedback on clarity, trade-offs, and maintainability."


def get_api_key() -> str | None:
    # Prefer Streamlit secrets, fall back to env.
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


@st.cache_resource
def cached_client(api_key: str | None):
    return build_client(api_key)


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🌸", layout="wide")
    inject_soft_sakura_css()

    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)

    with st.sidebar:
        st.subheader("Settings")

        model_name = st.selectbox(
            "Model",
            options=[
                "gemini-2.5-flash",
                "gemini-2.5-pro",
            ],
            index=0,
            help="Flash is faster/cheaper; Pro is stronger reasoning.",
        )

        temperature = st.slider("Determinism", 0.0, 1.0, 0.2, 0.05, help="Lower = more consistent.")

        st.divider()
        st.caption("Secrets")
        st.caption("Keep your API key in Streamlit secrets or environment variables.")

    api_key = get_api_key()
    if not api_key:
        st.warning(
            "Add your **GEMINI_API_KEY** in `.streamlit/secrets.toml` (local) "
            "or in the deployment secrets panel."
        )
        st.stop()

    client = cached_client(api_key)

    st.subheader("Input")
    colA, colB = st.columns([2, 1])

    with colA:
        code = st.text_area(
            "Paste code or a PR diff",
            height=320,
            placeholder="Paste your code here…\n\nTip: PR diffs work best if they include surrounding context.",
        )

    with colB:
        uploaded = st.file_uploader("Or upload a file", type=["py", "txt", "diff", "patch"])
        if uploaded is not None:
            try:
                code = uploaded.read().decode("utf-8", errors="replace")
                st.success("Loaded file into the text box.")
            except Exception:
                st.error("Could not read the uploaded file.")

        st.info(
            "This tool focuses on **design and maintainability**.\n"
            "It does not execute code."
        )

    run = st.button("Review calmly 🌸", type="primary", use_container_width=True, disabled=not bool(code.strip()))

    if run:
        with st.spinner("Reviewing with care…"):
            try:
                report = review_code(
                    client=client,
                    model_name=model_name,
                    code=code,
                    temperature=temperature,
                )
            except Exception as e:
                st.error("Something went wrong while generating the review.")
                st.exception(e)
                st.stop()

        st.subheader("Review")
        render_report(report)


if __name__ == "__main__":
    main()
