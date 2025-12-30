from __future__ import annotations

import os
from google import genai
from google.genai import types


def build_client(api_key: str | None) -> genai.Client:
    """
    Creates a Gemini Developer API client.
    Official SDK: google-genai.
    """
    if api_key:
        return genai.Client(api_key=api_key)
    # If api_key is not provided, the client can read GEMINI_API_KEY / GOOGLE_API_KEY from env.
    # (We still validate in the app for a better UX.)
    return genai.Client()


def build_json_config(response_schema: dict, temperature: float = 0.2, max_output_tokens: int = 1200) -> types.GenerateContentConfig:
    """
    Forces structured JSON output using response schema.
    Structured outputs: response_mime_type='application/json' + response_schema.
    """
    return types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        response_mime_type="application/json",
        response_schema=response_schema,
    )


def schema_from_pydantic(model) -> dict:
    """
    Pydantic v2 -> JSON schema dict.
    Gemini structured output accepts JSON schema dict.
    """
    return model.model_json_schema()


def generate_json_report(
    *,
    client: genai.Client,
    model_name: str,
    contents: str,
    config: types.GenerateContentConfig,
) -> str:
    """
    Calls Gemini and returns raw JSON string (response.text).
    """
    resp = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config,
    )
    return resp.text
