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
        self.assertGreater(len(self.frontmatter["description"]), 250)
        self.assertGreater(len(self.body), 2000)

    def test_description_covers_trigger_contexts(self) -> None:
        self.require_skill()
        description = self.frontmatter["description"].lower()

        required_terms = [
            "job",
            "github",
            "project",
            "learning roadmap",
            "resume",
            "interview",
            "job description",
            "repository evaluation",
        ]

        for term in required_terms:
            self.assertIn(term, description)

    def test_body_uses_strict_markdown_structure_and_critical_rules(self) -> None:
        self.require_skill()

        expected_headings = [
            "## Critical Rules",
            "## Inputs And Conflict Handling",
            "## Search Strategy",
            "## Repository Evaluation",
            "## Output Contract",
            "## Second-Development Guidance",
            "## Source Structure Review",
            "## Anti-Stall Learning Route",
            "## Resume And Interview Guidance",
        ]

        for heading in expected_headings:
            self.assertIn(heading, self.body)

        lower = self.body.lower()
        self.assertLess(self.body.index("## Critical Rules"), self.body.index("## Search Strategy"))
        self.assertIn("do not recommend projects only because they have many stars", lower)
        self.assertIn("do not fabricate", lower)
        self.assertIn("lower the recommendation confidence", lower)

    def test_body_contains_search_strategy_and_degraded_path(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "current github information",
            "degraded path",
            "repository links",
            "readme content",
            "trust the user's stated level",
            "spring boot",
            "docker-compose",
            "site:github.com",
            "awesome",
            "interview",
            "learning notes",
            "adjust the query",
        ]

        for term in required_terms:
            self.assertIn(term, lower)

    def test_body_contains_repository_evaluation_and_hallucination_boundaries(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "non-negotiable",
            "important signals",
            "bonus signals",
            "visible maintenance signals",
            "issue resolution rate",
            "pr merge rate",
            "maintainer response time",
            "without github rest api or graphql api",
            "do not claim exact",
            "not recommended and why",
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
            "Narrow Output Modes",
            "Project recommendations only",
            "Learning route only",
            "Resume-only",
            "Interview-only",
            "Single repository link",
        ]

        for section in required_sections:
            self.assertIn(section, self.body)

        self.assertIn("scale the schedule to the user's time budget", self.body)

    def test_body_contains_second_development_and_quantitative_baselines(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "business loop",
            "engineering quality",
            "architecture upgrade",
            "performance and reliability",
            "security and permissions",
            "deployment and observability",
            "at least two layers",
            "technical anchors",
            "redis",
            "kafka",
            "prometheus",
            "opentelemetry",
            "quantitative baseline",
            "expected target",
            "do not present expected targets as completed results",
            "p95",
        ]

        for term in required_terms:
            self.assertIn(term, lower)

    def test_body_contains_source_review_anti_stall_and_interview_defense(self) -> None:
        self.require_skill()
        lower = self.body.lower()

        required_terms = [
            "source structure review",
            "package.json",
            "pom.xml",
            "dockerfile",
            "docker-compose.yml",
            "anti-stall",
            "minimum startup path",
            "environment checklist",
            "common blockers",
            "timebox",
            "verification signal",
            "30 to 45 minutes",
            "1 to 2 hours",
            "trade-off",
            "pitfalls",
            "why this technology",
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
