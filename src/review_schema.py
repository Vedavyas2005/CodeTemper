from __future__ import annotations

from typing import List, Literal, Annotated
from pydantic import BaseModel, Field


# ---- constrained scalar types (no call expressions in annotations) ----
CognitiveLoadScore = Annotated[
    int,
    Field(
        ge=1,
        le=10,
        description="1 = very easy to understand, 10 = very hard"
    )
]


class Finding(BaseModel):
    title: str = Field(..., description="Short, human-readable title")
    severity: Literal["low", "medium", "high"] = Field(
        ...,
        description="Impact / risk level"
    )
    explanation: str = Field(
        ...,
        description="Calm, constructive explanation"
    )
    suggestion: str = Field(
        ...,
        description="Actionable suggestion"
    )


class CodeReviewReport(BaseModel):
    # ---- EXACT SAME FIELD NAMES AS BEFORE ----

    cognitive_load_score: CognitiveLoadScore
    cognitive_load_reason: str = Field(
        ...,
        description="Why the score is what it is"
    )

    pr_risk: Literal["low", "medium", "high"] = Field(
        ...,
        description="Overall risk if merged as-is"
    )
    pr_risk_reason: str = Field(
        ...,
        description="Why the risk is rated that way"
    )

    overengineering_flags: List[Finding] = Field(default_factory=list)
    future_breakage_risks: List[Finding] = Field(default_factory=list)
    readability_issues: List[Finding] = Field(default_factory=list)

    what_not_to_change: List[str] = Field(
        default_factory=list,
        description="Good decisions worth preserving"
    )

    senior_review_summary: str = Field(
        ...,
        description="Short PR-style summary in a calm senior voice"
    )
