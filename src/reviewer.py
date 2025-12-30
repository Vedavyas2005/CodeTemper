import json
from pydantic import ValidationError

from src.prompts import SYSTEM_STYLE, USER_TASK
from src.review_schema import CodeReviewReport
from src.gemini_client import (
    build_json_config,
    schema_from_pydantic,
    generate_json_report,
)


def build_prompt(code: str) -> str:
    # Keep the reviewer persona consistent and calm
    return (
        SYSTEM_STYLE.strip()
        + "\n\n"
        + USER_TASK.format(code=code).strip()
    )

def review_code(
    *,
    client,
    model_name: str,
    code: str,
    temperature: float = 0.2,
) -> CodeReviewReport:
    prompt = build_prompt(code)
    schema = schema_from_pydantic(CodeReviewReport)

    config = build_json_config(
        response_schema=schema,
        temperature=temperature,
        max_output_tokens=1200,  # slightly tighter
    )

    last_error = None

    for attempt in range(2):  # ONE retry only
        raw = generate_json_report(
            client=client,
            model_name=model_name,
            contents=prompt,
            config=config,
        )

        try:
            data = json.loads(raw)
            return CodeReviewReport.model_validate(data)
        except Exception as e:
            last_error = e
            # Ask Gemini to repair its own JSON
            prompt = (
                "The previous response was invalid JSON.\n"
                "Return ONLY a corrected JSON object matching the schema.\n\n"
                f"Previous output:\n{raw}"
            )

    raise RuntimeError(
        "Gemini did not return valid JSON after retry.\n\n"
        f"Last output:\n{raw}"
    ) from last_error