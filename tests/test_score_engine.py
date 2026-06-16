import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE_PATH = ROOT / "zero-to-job-project-coach" / "scripts" / "scoring_engine.py"


def load_engine_module():
    spec = importlib.util.spec_from_file_location("ztj_scoring_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("Unable to load scoring_engine.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload(
    *,
    evidence_level: str = "A",
    engineering: int = 20,
    stack: int = 20,
    learning_fit: int = 18,
    secondary_dev: int = 17,
    maintenance: int = 8,
    veto_reasons: list[str] | None = None,
    cap_reasons: list[str] | None = None,
):
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
        "engineering": dimension(engineering),
        "stack": dimension(stack),
        "learning_fit": dimension(learning_fit),
        "secondary_dev": dimension(secondary_dev),
        "maintenance": dimension(maintenance),
        "veto_reasons": veto_reasons or [],
        "cap_reasons": cap_reasons or [],
        "core_evidence": ["README 可见启动说明"],
        "major_risks": ["源码结构仍需进一步深查"],
        "next_steps": ["验证 3-5 个关键接口"],
    }


class ScoreEngineTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.engine = load_engine_module()

    def score(self, payload: dict):
        return self.engine.score_project(payload)

    def test_veto_forces_not_recommended_and_na_score(self) -> None:
        result = self.score(build_payload(veto_reasons=["缺乏核心源码"]))
        self.assertEqual(result["final_conclusion"], "不推荐")
        self.assertEqual(result["total_score"], 0)
        self.assertEqual(result["display_score"], "N/A")
        self.assertIn("命中一票否决，分数作废", result["applied_adjustments"])

    def test_raw_score_maps_to_strong_recommendation(self) -> None:
        result = self.score(build_payload(engineering=22, stack=23, learning_fit=18, secondary_dev=16, maintenance=8))
        self.assertEqual(result["raw_conclusion"], "强烈推荐")
        self.assertEqual(result["final_conclusion"], "强烈推荐")

    def test_raw_score_maps_to_recommended_with_risk(self) -> None:
        result = self.score(build_payload(engineering=18, stack=18, learning_fit=15, secondary_dev=13, maintenance=7))
        self.assertEqual(result["raw_conclusion"], "推荐但有风险")
        self.assertEqual(result["final_conclusion"], "推荐但有风险")

    def test_raw_score_maps_to_not_recommended(self) -> None:
        result = self.score(build_payload(engineering=10, stack=12, learning_fit=12, secondary_dev=10, maintenance=5))
        self.assertEqual(result["raw_conclusion"], "不推荐")
        self.assertEqual(result["final_conclusion"], "不推荐")

    def test_c_evidence_caps_conclusion_to_recommended_with_risk(self) -> None:
        result = self.score(
            build_payload(
                evidence_level="C",
                engineering=22,
                stack=22,
                learning_fit=18,
                secondary_dev=17,
                maintenance=8,
            )
        )
        self.assertEqual(result["raw_conclusion"], "强烈推荐")
        self.assertEqual(result["final_conclusion"], "推荐但有风险")
        self.assertEqual(result["display_score"], result["total_score"])
        self.assertIn("C级证据结论封顶为推荐但有风险", result["applied_adjustments"])

    def test_c_score_of_75_does_not_trigger_extra_score_adjustment(self) -> None:
        result = self.score(
            build_payload(
                evidence_level="C",
                engineering=20,
                stack=20,
                learning_fit=15,
                secondary_dev=13,
                maintenance=7,
            )
        )
        self.assertEqual(result["total_score"], 75)
        self.assertEqual(result["raw_conclusion"], "推荐但有风险")
        self.assertEqual(result["final_conclusion"], "推荐但有风险")
        self.assertNotIn("C级证据分数封顶至75", result["applied_adjustments"])

    def test_b_high_score_has_no_adjustment(self) -> None:
        result = self.score(build_payload(evidence_level="B", engineering=22, stack=22, learning_fit=18, secondary_dev=18, maintenance=10))
        self.assertEqual(result["final_conclusion"], "强烈推荐")
        self.assertEqual(result["applied_adjustments"], [])

    def test_b_plus_does_not_trigger_c_adjustment(self) -> None:
        result = self.score(build_payload(evidence_level="B+", engineering=22, stack=22, learning_fit=18, secondary_dev=18, maintenance=10))
        self.assertEqual(result["final_conclusion"], "强烈推荐")
        self.assertNotIn("C级证据结论封顶为推荐但有风险", result["applied_adjustments"])

    def test_cap_reasons_force_recommended_with_risk(self) -> None:
        result = self.score(
            build_payload(
                engineering=22,
                stack=22,
                learning_fit=18,
                secondary_dev=18,
                maintenance=10,
                cap_reasons=["README 很完整，但源码结构混乱"],
            )
        )
        self.assertEqual(result["raw_conclusion"], "强烈推荐")
        self.assertEqual(result["final_conclusion"], "推荐但有风险")
        self.assertIn("命中禁止高分场景，结论封顶为推荐但有风险", result["applied_adjustments"])

    def test_cap_reason_on_not_recommended_adds_no_adjustment(self) -> None:
        result = self.score(
            build_payload(
                engineering=10,
                stack=12,
                learning_fit=12,
                secondary_dev=10,
                maintenance=5,
                cap_reasons=["项目可以运行，但二次开发空间很弱"],
            )
        )
        self.assertEqual(result["final_conclusion"], "不推荐")
        self.assertEqual(result["applied_adjustments"], [])

    def test_veto_wins_over_cap(self) -> None:
        result = self.score(
            build_payload(
                veto_reasons=["长期未维护且无法运行"],
                cap_reasons=["README 很完整，但源码结构混乱"],
            )
        )
        self.assertEqual(result["final_conclusion"], "不推荐")
        self.assertEqual(result["applied_adjustments"], ["命中一票否决，分数作废"])

    def test_c_and_cap_both_record_adjustments(self) -> None:
        result = self.score(
            build_payload(
                evidence_level="C",
                engineering=22,
                stack=22,
                learning_fit=18,
                secondary_dev=18,
                maintenance=10,
                cap_reasons=["技术栈豪华，但业务闭环不明确"],
            )
        )
        self.assertEqual(result["final_conclusion"], "推荐但有风险")
        self.assertEqual(
            result["applied_adjustments"],
            [
                "C级证据结论封顶为推荐但有风险",
                "命中禁止高分场景，结论封顶为推荐但有风险",
            ],
        )

    def test_invalid_evidence_level_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.score(build_payload(evidence_level="D"))

    def test_dimension_score_out_of_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            self.score(build_payload(engineering=26))

    def test_empty_evidence_summary_raises(self) -> None:
        payload = build_payload()
        payload["engineering"]["evidence_summary"] = ""
        with self.assertRaises(ValueError):
            self.score(payload)

    def test_empty_deduction_reason_raises(self) -> None:
        payload = build_payload()
        payload["engineering"]["deduction_reason"] = ""
        with self.assertRaises(ValueError):
            self.score(payload)
