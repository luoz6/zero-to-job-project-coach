from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "zero-to-job-project-coach"
SKILL_MD = SKILL_DIR / "SKILL.md"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"
REFERENCES_DIR = SKILL_DIR / "references"

REFERENCE_FILES = {
    "role_templates": REFERENCES_DIR / "role_templates.md",
    "github_scoring_matrix": REFERENCES_DIR / "github_scoring_matrix.md",
    "secondary_dev_blueprints": REFERENCES_DIR / "secondary_dev_blueprints.md",
    "resume_benchmarks": REFERENCES_DIR / "resume_benchmarks.md",
    "job_execution_playbook": REFERENCES_DIR / "job_execution_playbook.md",
}

BEHAVIOR_EVALS = ROOT / "tests" / "behavior_eval_cases.md"


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
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter, body


def parse_openai_interface(text: str) -> dict[str, str]:
    # This intentionally supports only the simple interface contract used here.
    # If openai.yaml grows multiline YAML values, replace this with yaml.safe_load.
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


class ZeroToJobProjectCoachV2Test(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_text = read_text(SKILL_MD)
        self.frontmatter, self.body = parse_frontmatter(self.skill_text)

    def assert_contains_all(self, text: str, terms: list[str]) -> None:
        lower = text.lower()
        for term in terms:
            self.assertIn(term.lower(), lower)

    def test_frontmatter_and_openai_yaml(self) -> None:
        self.assertEqual(set(self.frontmatter), {"name", "description"})
        self.assertEqual(self.frontmatter["name"], "zero-to-job-project-coach")
        self.assertIn("从 0 到找工作", self.frontmatter["description"])
        self.assertGreater(len(self.body), 2000)

        interface = parse_openai_interface(read_text(OPENAI_YAML))
        self.assertEqual(interface.get("display_name"), "Zero To Job Project Coach")
        self.assertRegex(interface.get("short_description", ""), r"^.{20,120}$")
        self.assertRegex(interface.get("default_prompt", ""), r"^Use \$zero-to-job-project-coach .+")
        self.assert_contains_all(
            interface.get("default_prompt", ""),
            ["阶段诊断", "项目选择", "二次开发", "简历", "面试"],
        )

    def test_references_exist(self) -> None:
        self.assertTrue(REFERENCES_DIR.is_dir(), "references directory should exist")
        for path in REFERENCE_FILES.values():
            self.assertTrue(path.is_file(), f"{path.name} should exist")

    def test_skill_is_v2_control_engine(self) -> None:
        required_headings = [
            "## 关键规则",
            "## 输入与冲突处理",
            "## Reference 调度规则",
            "## Reference 输出边界",
            "## 状态管理与阶段声明",
            "## 三阶段解锁工作流",
            "## Phase 1：诊断、拆解与选型定调",
            "## Phase 2：硬核开模与验收标准",
            "## Phase 3：交付转化与求职冲刺",
            "## 私有/企业项目处理",
            "## 阶段卡点与推进条件",
            "## 验收失败纠偏机制",
            "## 降级路径",
            "## 输出控制",
        ]
        for heading in required_headings:
            self.assertIn(heading, self.body)

        self.assertLess(self.body.index("## 关键规则"), self.body.index("## Reference 调度规则"))
        self.assertLess(self.body.index("## Reference 调度规则"), self.body.index("## 三阶段解锁工作流"))

        self.assert_contains_all(
            self.body,
            [
                "references/role_templates.md",
                "references/github_scoring_matrix.md",
                "references/secondary_dev_blueprints.md",
                "references/resume_benchmarks.md",
                "references/job_execution_playbook.md",
                "[当前阶段：Phase X - 简短状态]",
                "不承诺 offer",
                "不得只因为 star 多",
                "不得编造 issue 解决率",
                "不得把建议改造",
                "按需读取 reference",
                "唯一真理",
                "严禁使用预训练数据自行发散或降低标准",
                "Phase 1 不输出高压追问",
                "Phase 2 不提前生成正式简历 bullet",
                "低风险默认假设",
                "高风险追问",
                "水平/JD 冲突",
                "未通过验收，不建议直接写进正式简历",
                "私有仓库",
                "不得要求用户泄露公司敏感信息",
                "跳过卡点",
                "待验证",
                "源码结构评估结论",
                "明确卡点提问",
                "最小 Phase 1",
                '用户场景"学习路线"',
                '用户场景"单个仓库链接"',
            ],
        )

    def test_role_templates_reference(self) -> None:
        text = read_text(REFERENCE_FILES["role_templates"])
        self.assert_contains_all(
            text,
            [
                "Java 后端",
                "前端",
                "AI 应用开发",
                "数据分析",
                "DevOps",
                "全栈",
                "移动端开发",
                "底层基线",
                "进阶能力",
                "推荐项目类型",
                "最低简历项目标准",
                "里程碑验收问题",
                "Spring Boot",
                "MyBatis",
                "AOP",
                "Redis",
                "消息队列",
                "RAG",
                "LangChain",
                "向量数据库",
                "TextSplitter",
                "进阶验收点",
            ],
        )

    def test_github_scoring_matrix_reference(self) -> None:
        text = read_text(REFERENCE_FILES["github_scoring_matrix"])
        self.assert_contains_all(
            text,
            [
                "满分 100 分",
                "工程规范度 25 分",
                "技术栈含金量 25 分",
                "学习价值与阶段匹配 20 分",
                "二次开发空间 20 分",
                "可见维护信号 10 分",
                "一票否决",
                "学习笔记",
                "awesome list",
                "不得编造",
                "issue 解决率",
                "PR 合并率",
                "阶段匹配扣分锚点",
                "至少扣 15 分",
                "至少扣 10 分",
                "降级学习路线",
                "搜索策略",
                "site:github.com",
                "spring boot redis docker-compose ecommerce OR mall",
                "排除关键词",
                "interview",
                "notes",
                "候选结果质量差",
                "调整查询后重新搜索",
                "宽泛查询",
                "精准信号组合",
                "仓库评估：10-15 分钟/个",
            ],
        )

    def test_secondary_dev_blueprints_reference(self) -> None:
        text = read_text(REFERENCE_FILES["secondary_dev_blueprints"])
        self.assert_contains_all(
            text,
            [
                "Level 1",
                "Level 2",
                "Level 3",
                "业务闭环",
                "架构与高并发",
                "治理与性能",
                "Caffeine + Redis",
                "Canal",
                "RocketMQ",
                "动态线程池",
                "Prometheus",
                "OpenTelemetry",
                "适用场景",
                "技术锚点",
                "改造步骤",
                "可交付物",
                "验收问题",
                "简历表达模板",
                "2 小时",
                "45 分钟",
                "0.5-2 天",
                "0.5 天",
            ],
        )

    def test_resume_benchmarks_reference(self) -> None:
        text = read_text(REFERENCE_FILES["resume_benchmarks"])
        self.assert_contains_all(
            text,
            [
                "STAR",
                "低效表达",
                "高阶表达",
                "Java 后端",
                "前端",
                "AI 应用开发",
                "预期目标",
                "完成后待实测",
                "不得写成已完成结果",
                "场景",
                "技术选型",
                "指标来源",
                "踩坑",
                "回滚方案",
            ],
        )

    def test_job_execution_playbook_reference(self) -> None:
        text = read_text(REFERENCE_FILES["job_execution_playbook"])
        self.assert_contains_all(
            text,
            [
                "高压追问",
                "技术选型与踩坑",
                "投递执行表",
                "Markdown 表格",
                "CSV 代码块",
                "日期",
                "岗位",
                "公司分层",
                "简历版本",
                "投递渠道",
                "反馈",
                "盲区",
                "1 到 2 周",
                "面试复盘",
            ],
        )

    def test_behavior_eval_cases_exist(self) -> None:
        self.assertTrue(BEHAVIOR_EVALS.is_file(), "behavior eval cases should exist")
        text = read_text(BEHAVIOR_EVALS)
        self.assert_contains_all(
            text,
            [
                "跳过 Phase 2",
                "未完成实操带来的简历风险",
                "Phase 1 后未确认项目",
                "先确认项目",
                "私有实习项目",
                "跳过 GitHub scoring",
                "验收问题错误",
                "给 Hint",
                "不直接进入 Phase 3",
                "投递计划",
                "Markdown 表格",
                "CSV 代码块",
                "静态行为评测基线",
                "不是自动化模型评测",
            ],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
