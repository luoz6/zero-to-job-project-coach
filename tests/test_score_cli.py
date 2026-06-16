import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = ROOT / "zero-to-job-project-coach" / "scripts" / "score.py"
PYTHON = Path(r"F:\python3.11\python.exe")


def build_payload(veto_reasons=None, cap_reasons=None, evidence_level="A"):
    def dimension(score: int) -> dict:
        return {
            "score": score,
            "evidence_summary": "有可见证据支持该维评分",
            "deduction_reason": "无明显扣分项",
        }

    return {
        "project_name": "demo-project",
        "repo_url": "https://github.com/example/demo-project",
        "evidence_level": evidence_level,
        "engineering": dimension(22),
        "stack": dimension(22),
        "learning_fit": dimension(18),
        "secondary_dev": dimension(18),
        "maintenance": dimension(10),
        "veto_reasons": veto_reasons or [],
        "cap_reasons": cap_reasons or [],
        "core_evidence": ["README 可见启动说明"],
        "major_risks": ["源码结构仍需进一步深查"],
        "next_steps": ["验证 3-5 个关键接口"],
    }


class ScoreCliTest(unittest.TestCase):
    def run_cli(self, payload: dict) -> str:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "input.json"
            input_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            result = subprocess.run(
                [str(PYTHON), str(CLI_PATH), str(input_path)],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            return result.stdout

    def test_cli_reads_json_and_prints_markdown(self) -> None:
        output = self.run_cli(build_payload())
        self.assertIn("| 字段 | 内容 |", output)
        self.assertIn("| 评分维度 | 得分 | 证据摘要 | 扣分原因 |", output)
        self.assertIn("demo-project", output)

    def test_cli_uses_na_when_vetoed(self) -> None:
        output = self.run_cli(build_payload(veto_reasons=["缺乏核心源码"]))
        self.assertIn("| 总分 | N/A |", output)
        self.assertIn("| 结论 | 不推荐 |", output)

    def test_cli_outputs_rule_adjustments_section(self) -> None:
        output = self.run_cli(build_payload(evidence_level="C", cap_reasons=["README 很完整，但源码结构混乱"]))
        self.assertIn("### 规则修正", output)
        self.assertIn("C级证据结论封顶为推荐但有风险", output)
        self.assertIn("命中禁止高分场景，结论封顶为推荐但有风险", output)
