from typing import Any


VALID_EVIDENCE_LEVELS = {"A", "B+", "B", "C"}
DIMENSION_LIMITS = {
    "engineering": 25,
    "stack": 25,
    "learning_fit": 20,
    "secondary_dev": 20,
    "maintenance": 10,
}
DIMENSION_LABELS = {
    "engineering": "工程规范度",
    "stack": "技术栈含金量",
    "learning_fit": "学习价值与阶段匹配",
    "secondary_dev": "二次开发空间",
    "maintenance": "可见维护信号",
}


class DimensionScore:
    def __init__(self, score: int, evidence_summary: str, deduction_reason: str) -> None:
        self.score = score
        self.evidence_summary = evidence_summary
        self.deduction_reason = deduction_reason

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "evidence_summary": self.evidence_summary,
            "deduction_reason": self.deduction_reason,
        }


class ScoreInput:
    def __init__(
        self,
        *,
        project_name: str,
        repo_url: str,
        evidence_level: str,
        engineering: DimensionScore,
        stack: DimensionScore,
        learning_fit: DimensionScore,
        secondary_dev: DimensionScore,
        maintenance: DimensionScore,
        veto_reasons: list[str],
        cap_reasons: list[str],
        core_evidence: list[str],
        major_risks: list[str],
        next_steps: list[str],
    ) -> None:
        self.project_name = project_name
        self.repo_url = repo_url
        self.evidence_level = evidence_level
        self.engineering = engineering
        self.stack = stack
        self.learning_fit = learning_fit
        self.secondary_dev = secondary_dev
        self.maintenance = maintenance
        self.veto_reasons = veto_reasons
        self.cap_reasons = cap_reasons
        self.core_evidence = core_evidence
        self.major_risks = major_risks
        self.next_steps = next_steps


def _require_non_empty_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _require_string_list(value: Any, field_name: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list of strings")
    cleaned: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name}[{index}] must be a non-empty string")
        cleaned.append(item.strip())
    return cleaned


def _parse_dimension(name: str, data: Any) -> DimensionScore:
    if not isinstance(data, dict):
        raise ValueError(f"{name} must be an object")

    score = data.get("score")
    if not isinstance(score, int):
        raise ValueError(f"{name}.score must be an integer")
    if score < 0 or score > DIMENSION_LIMITS[name]:
        raise ValueError(f"{name}.score must be between 0 and {DIMENSION_LIMITS[name]}")

    evidence_summary = _require_non_empty_string(data.get("evidence_summary"), f"{name}.evidence_summary")
    deduction_reason = _require_non_empty_string(data.get("deduction_reason"), f"{name}.deduction_reason")
    return DimensionScore(score=score, evidence_summary=evidence_summary, deduction_reason=deduction_reason)


def validate_input(data: dict[str, Any]) -> ScoreInput:
    if not isinstance(data, dict):
        raise ValueError("input must be an object")

    evidence_level = _require_non_empty_string(data.get("evidence_level"), "evidence_level")
    if evidence_level not in VALID_EVIDENCE_LEVELS:
        raise ValueError("evidence_level must be one of A, B+, B, C")

    return ScoreInput(
        project_name=_require_non_empty_string(data.get("project_name"), "project_name"),
        repo_url=_require_non_empty_string(data.get("repo_url"), "repo_url"),
        evidence_level=evidence_level,
        engineering=_parse_dimension("engineering", data.get("engineering")),
        stack=_parse_dimension("stack", data.get("stack")),
        learning_fit=_parse_dimension("learning_fit", data.get("learning_fit")),
        secondary_dev=_parse_dimension("secondary_dev", data.get("secondary_dev")),
        maintenance=_parse_dimension("maintenance", data.get("maintenance")),
        veto_reasons=_require_string_list(data.get("veto_reasons", []), "veto_reasons"),
        cap_reasons=_require_string_list(data.get("cap_reasons", []), "cap_reasons"),
        core_evidence=_require_string_list(data.get("core_evidence", []), "core_evidence"),
        major_risks=_require_string_list(data.get("major_risks", []), "major_risks"),
        next_steps=_require_string_list(data.get("next_steps", []), "next_steps"),
    )


def compute_raw_total(score_input: ScoreInput) -> int:
    return (
        score_input.engineering.score
        + score_input.stack.score
        + score_input.learning_fit.score
        + score_input.secondary_dev.score
        + score_input.maintenance.score
    )


def map_conclusion(total_score: int) -> str:
    if total_score >= 85:
        return "强烈推荐"
    if total_score >= 70:
        return "推荐但有风险"
    return "不推荐"


def render_markdown(score_input: ScoreInput, result: dict[str, Any]) -> str:
    overview_lines = [
        "### 结论总览表",
        "",
        "| 字段 | 内容 |",
        "| --- | --- |",
        f"| 项目名 / 仓库链接 | `{score_input.project_name}` / `{score_input.repo_url}` |",
        f"| 总分 | {result['display_score']} |",
        f"| 证据等级 | {score_input.evidence_level} |",
        f"| 结论 | {result['final_conclusion']} |",
        "",
        "### 分项评分表",
        "",
        "| 评分维度 | 得分 | 证据摘要 | 扣分原因 |",
        "| --- | --- | --- | --- |",
    ]

    for key in ["engineering", "stack", "learning_fit", "secondary_dev", "maintenance"]:
        dimension = getattr(score_input, key)
        overview_lines.append(
            f"| {DIMENSION_LABELS[key]} | {dimension.score}/{DIMENSION_LIMITS[key]} | {dimension.evidence_summary} | {dimension.deduction_reason} |"
        )

    if result["applied_adjustments"]:
        overview_lines.extend(["", "### 规则修正", ""])
        for item in result["applied_adjustments"]:
            overview_lines.append(f"- {item}")

    overview_lines.extend(["", "### 核心证据", ""])
    overview_lines.extend(f"- {item}" for item in score_input.core_evidence)
    overview_lines.extend(["", "### 主要风险", ""])
    overview_lines.extend(f"- {item}" for item in score_input.major_risks)
    overview_lines.extend(["", "### 下一步建议", ""])
    overview_lines.extend(f"- {item}" for item in score_input.next_steps)
    overview_lines.append("")
    return "\n".join(overview_lines)


def build_json_report(score_input: ScoreInput, result: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "input": {
                "project_name": score_input.project_name,
                "repo_url": score_input.repo_url,
                "evidence_level": score_input.evidence_level,
                "dimensions": {
                    "engineering": score_input.engineering.to_dict(),
                    "stack": score_input.stack.to_dict(),
                    "learning_fit": score_input.learning_fit.to_dict(),
                    "secondary_dev": score_input.secondary_dev.to_dict(),
                    "maintenance": score_input.maintenance.to_dict(),
                },
            "veto_reasons": score_input.veto_reasons,
            "cap_reasons": score_input.cap_reasons,
            "core_evidence": score_input.core_evidence,
            "major_risks": score_input.major_risks,
            "next_steps": score_input.next_steps,
        },
        "result": {
            "total_score": result["total_score"],
            "display_score": result["display_score"],
            "raw_conclusion": result["raw_conclusion"],
            "final_conclusion": result["final_conclusion"],
            "applied_adjustments": result["applied_adjustments"],
        },
    }
    return payload


def score_project(data: dict[str, Any]) -> dict[str, Any]:
    score_input = validate_input(data)

    if score_input.veto_reasons:
        result = {
            "total_score": 0,
            "display_score": "N/A",
            "raw_conclusion": "不推荐",
            "final_conclusion": "不推荐",
            "applied_adjustments": ["命中一票否决，分数作废"],
        }
        result["markdown_report"] = render_markdown(score_input, result)
        result["json_report"] = build_json_report(score_input, result)
        return result

    total_score = compute_raw_total(score_input)
    display_score: int | str = total_score
    raw_conclusion = map_conclusion(total_score)
    final_conclusion = raw_conclusion
    applied_adjustments: list[str] = []

    if score_input.evidence_level == "C" and raw_conclusion == "强烈推荐":
        final_conclusion = "推荐但有风险"
        applied_adjustments.append("C级证据结论封顶为推荐但有风险")

    if score_input.cap_reasons and raw_conclusion == "强烈推荐":
        final_conclusion = "推荐但有风险"
        applied_adjustments.append("命中禁止高分场景，结论封顶为推荐但有风险")

    result = {
        "total_score": total_score,
        "display_score": display_score,
        "raw_conclusion": raw_conclusion,
        "final_conclusion": final_conclusion,
        "applied_adjustments": applied_adjustments,
    }
    result["markdown_report"] = render_markdown(score_input, result)
    result["json_report"] = build_json_report(score_input, result)
    return result
