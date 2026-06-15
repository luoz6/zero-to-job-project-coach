from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "github-career-project-planner"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.replace("\r\n", "\n")

    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")

    end = text.find("\n---\n", 4)
    if end == -1:
        raise AssertionError("SKILL.md frontmatter must be closed with ---")

    raw_frontmatter = text[4:end]
    body = text[end + len("\n---\n") :]
    frontmatter: dict[str, str] = {}

    for line in raw_frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise AssertionError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"')

    return frontmatter, body


def parse_openai_interface(text: str) -> dict[str, str]:
    interface: dict[str, str] = {}
    in_interface = False

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "interface:":
            in_interface = True
            continue
        if in_interface and raw_line[:1].strip() and not raw_line.startswith((" ", "\t")):
            break
        if not in_interface or ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        interface[key.strip()] = value.strip().strip('"').strip("'")

    return interface


class GitHubCareerProjectPlannerSkillTest(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = ""
        self.frontmatter: dict[str, str] = {}
        self.body = ""

        if SKILL_MD.is_file():
            self.skill_text = read_text(SKILL_MD)
            self.frontmatter, self.body = parse_frontmatter(self.skill_text)

    def require_skill(self) -> None:
        if not SKILL_DIR.is_dir():
            self.skipTest("SKILL.md not created yet; structure test covers this")
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md should exist")

    def require_openai_yaml(self) -> None:
        if not SKILL_DIR.is_dir():
            self.skipTest("agents/openai.yaml not created yet")
        self.assertTrue(OPENAI_YAML.is_file(), "agents/openai.yaml should exist")

    def test_skill_files_exist_and_frontmatter_contract(self) -> None:
        self.assertTrue(SKILL_DIR.is_dir(), "skill directory should exist")
        self.assertTrue(SKILL_MD.is_file(), "SKILL.md should exist")

        self.assertEqual(set(self.frontmatter), {"name", "description"})
        self.assertEqual(self.frontmatter["name"], "github-career-project-planner")
        self.assertGreater(len(self.frontmatter["description"]), 100)
        self.assertGreater(len(self.body), 2000)

    def test_description_covers_trigger_contexts(self) -> None:
        self.require_skill()
        description = self.frontmatter["description"].lower()

        required_terms = [
            "岗位",
            "github",
            "项目",
            "学习路线",
            "简历",
            "面试",
            "jd",
            "仓库评估",
        ]

        for term in required_terms:
            self.assertIn(term, description)

    def test_body_uses_strict_markdown_structure_and_critical_rules(self) -> None:
        self.require_skill()

        expected_headings = [
            "## 关键规则",
            "## 输入与冲突处理",
            "## 搜索策略",
            "## 仓库评估",
            "## 输出契约",
            "## 二次开发指导",
            "## 源码结构评估",
            "## 防卡壳学习路线",
            "## 简历与面试指导",
        ]

        for heading in expected_headings:
            self.assertIn(heading, self.body)

        lower = self.body.lower()
        self.assertLess(self.body.index("## 关键规则"), self.body.index("## 搜索策略"))
        self.assertIn("不得只因为 star 多就推荐项目", lower)
        self.assertIn("不得编造", lower)
        self.assertIn("降低推荐置信度", lower)

    def test_body_contains_search_strategy_and_degraded_path(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "当前 github 信息",
            "降级路径",
            "仓库链接",
            "readme 内容",
            "优先相信用户自述水平",
            "spring boot",
            "docker compose",
            "site:github.com",
            "awesome",
            "interview",
            "learning notes",
            "调整查询",
        ]

        for term in required_terms:
            self.assertIn(term, lower)

    def test_body_contains_repository_evaluation_and_hallucination_boundaries(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "不可妥协维度",
            "重要维度",
            "加分维度",
            "可见维护信号",
            "issue 解决率",
            "pr 合并率",
            "维护者响应时间",
            "没有 github rest api 或 graphql api",
            "不得声称精确统计",
            "明确不推荐及原因",
        ]

        for term in required_terms:
            self.assertIn(term, lower)

    def test_body_contains_output_contract_and_narrow_modes(self) -> None:
        self.require_skill()

        required_sections = [
            "岗位能力拆解",
            "GitHub 项目推荐",
            "不推荐及原因",
            "项目学习路线",
            "二次开发任务",
            "简历项目描述",
            "面试准备问题",
            "下一步行动计划",
            "窄输出模式",
            "只要项目推荐",
            "只要学习路线",
            "只要简历描述",
            "只要面试准备",
            "单个仓库链接",
        ]

        for section in required_sections:
            self.assertIn(section, self.body)

        self.assertIn("根据用户时间预算缩放计划", self.body)

    def test_body_contains_second_development_and_quantitative_baselines(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "业务闭环",
            "工程质量",
            "架构升级",
            "性能与可靠性",
            "安全与权限",
            "部署与可观测性",
            "至少覆盖两层",
            "技术锚点",
            "redis",
            "kafka",
            "prometheus",
            "opentelemetry",
            "量化基准",
            "预期目标",
            "不得把预期目标写成已完成结果",
            "p95",
        ]

        for term in required_terms:
            self.assertIn(term, lower)

    def test_body_contains_source_review_anti_stall_and_interview_defense(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "源码结构评估",
            "package.json",
            "pom.xml",
            "dockerfile",
            "docker-compose.yml",
            "防卡壳",
            "最小启动路径",
            "环境检查清单",
            "常见卡点",
            "时间盒",
            "验收信号",
            "30 到 45 分钟",
            "1 到 2 小时",
            "技术选型",
            "踩坑",
            "为什么选择这个技术",
        ]

        for term in required_terms:
            self.assertIn(term, lower)

    def test_openai_yaml_interface_contract(self) -> None:
        self.require_openai_yaml()
        yaml_text = read_text(OPENAI_YAML)
        self.assertIn("interface:", yaml_text)
        interface = parse_openai_interface(yaml_text)

        self.assertEqual(interface.get("display_name"), "GitHub Career Project Planner")
        self.assertRegex(interface.get("short_description", ""), r"^.{20,120}$")
        self.assertRegex(
            interface.get("default_prompt", ""),
            r"^Use \$github-career-project-planner .+",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
