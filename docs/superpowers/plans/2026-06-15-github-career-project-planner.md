# GitHub Career Project Planner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 `github-career-project-planner` skill，使 Codex 能根据目标岗位搜索并评估 GitHub 项目，生成学习路线、二次开发方案、简历项目描述和面试准备内容。

**Architecture:** 第一版只实现 skill 文档、UI 元数据和测试，不实现 GitHub API 客户端或自动评分脚本。测试使用 Python 标准库 `unittest` 验证文件结构、frontmatter、关键规则、输出契约和 `agents/openai.yaml` 元数据。

**Tech Stack:** Codex skill markdown, YAML metadata, Python `unittest`, local `skill-creator` scripts.

---

## File Structure

- Create: `tests/test_github_career_project_planner.py`
  - 负责 TDD 验证 skill 目录、`SKILL.md` frontmatter、正文关键规则、输出契约和 `agents/openai.yaml` 元数据。
- Create: `github-career-project-planner/SKILL.md`
  - 负责实际 skill 指令，使用严格 Markdown 层级，`Critical Rules` 放在正文前部。
- Create: `github-career-project-planner/agents/openai.yaml`
  - 负责 UI 展示元数据，使用本地规范确认过的 `interface.display_name`、`interface.short_description`、`interface.default_prompt`。
- Use: `C:\Users\admin\.codex\skills\.system\skill-creator\scripts\init_skill.py`
  - 初始化 skill 目录，符合 skill-creator “新建 skill 必须使用 init_skill.py” 的约束。虽然后续会替换模板内容，但保留该步骤可以确保目录结构和基础元数据生成流程遵循本地 skill 规范。
- Use: `C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py`
  - 验证 skill frontmatter 和命名规则。

当前目录 `F:\agent\skill` 不是 Git 仓库；执行阶段先通过 Task 0 初始化 Git 安全网并提交当前规格/计划。后续每个任务完成后可以提交一次，降低超长文档写坏后的回滚成本。本计划文件已在规划阶段创建，执行阶段不需要再次创建 `docs/superpowers/plans/2026-06-15-github-career-project-planner.md`。

本仓库当前执行环境是 PowerShell，因此命令使用 PowerShell 语法。如果执行者在 Bash、WSL 或其他 shell 中执行本计划，应先把命令等价转换，再运行。

### Task 0: 初始化版本控制安全网

**Files:**
- Verify: `docs/superpowers/specs/2026-06-15-github-career-project-planner-design.md`
- Verify: `docs/superpowers/plans/2026-06-15-github-career-project-planner.md`

- [ ] **Step 1: Initialize git repository if needed**

Run:

```powershell
if (-not (Test-Path -LiteralPath '.git')) { git init }
```

Expected: `.git` exists.

- [ ] **Step 2: Confirm no invisible characters in the plan**

Run:

```powershell
$text = Get-Content -Raw -Encoding UTF8 -LiteralPath 'docs\superpowers\plans\2026-06-15-github-career-project-planner.md'
$bad = @()
for ($i = 0; $i -lt $text.Length; $i++) {
  $code = [int][char]$text[$i]
  if ($code -eq 8203 -or $code -eq 65279) {
    $bad += [pscustomobject]@{ Index = $i; Code = $code }
  }
}
if ($bad.Count -gt 0) { $bad | Format-Table -AutoSize; exit 1 }
'NO_INVISIBLE_CHARS'
```

Expected: `NO_INVISIBLE_CHARS`.

- [ ] **Step 3: Commit the planning baseline**

Run:

```powershell
git add docs/superpowers/specs/2026-06-15-github-career-project-planner-design.md docs/superpowers/plans/2026-06-15-github-career-project-planner.md
git commit -m "docs: add github career project planner spec and plan"
```

Expected: baseline commit exists. If Git user identity is not configured, set local identity or skip commit with a note; do not block skill implementation.

### Task 1: 写失败测试

**Files:**
- Create: `tests/test_github_career_project_planner.py`

- [ ] **Step 1: Create tests directory**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'tests' | Out-Null
```

Expected: `tests` directory exists.

- [ ] **Step 2: Write the failing test file**

Create `tests/test_github_career_project_planner.py` with the Codex `apply_patch` edit tool, or an equivalent structured file-edit tool in another agent runtime. Do not use `echo`, `Set-Content`, `Out-File`, shell redirection, or heredoc-style shell writing for this file; those approaches are more likely to introduce encoding, quoting, or invisible-character problems.

Use this content:

```python
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
```

- [ ] **Step 3: Run test to verify it fails**

Run:

```powershell
python tests/test_github_career_project_planner.py
```

Expected: FAIL. The first failure should mention `skill directory should exist` because `github-career-project-planner/` has not been created yet.

### Task 2: 初始化 skill 目录并确认元数据格式

**Files:**
- Create: `github-career-project-planner/SKILL.md`
- Create: `github-career-project-planner/agents/openai.yaml`

- [ ] **Step 1: Confirm local openai.yaml field format**

Run:

```powershell
Get-Content -Encoding UTF8 -LiteralPath 'C:\Users\admin\.codex\skills\.system\skill-creator\references\openai_yaml.md'
```

Expected: The document shows `interface.display_name`, `interface.short_description`, and `interface.default_prompt`.

If the local reference instead shows a different schema, such as flat `name`, `description`, or `prompt` keys, stop before running `init_skill.py` and update both:

- `tests/test_github_career_project_planner.py::test_openai_yaml_interface_contract`
- Task 4 `openai.yaml` content

Use the local `openai_yaml.md` schema as the source of truth. Do not force the `interface.*` schema if the installed skill-creator reference disagrees.

- [ ] **Step 2: Confirm skill-creator script CLI usage**

Run:

```powershell
python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\init_skill.py' --help
python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py' --help
```

Expected: `init_skill.py` supports `--path` and repeated `--interface key=value`; `quick_validate.py` accepts a skill folder path.

If the installed script help differs, adjust Task 2 Step 3 and Task 5 commands to match the local CLI before running them.

- [ ] **Step 3: Initialize the skill with skill-creator**

Run:

```powershell
python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\init_skill.py' github-career-project-planner --path . --interface 'display_name=GitHub Career Project Planner' --interface 'short_description=Find job-targeted GitHub projects' --interface 'default_prompt=Use $github-career-project-planner to find GitHub projects for my target job and turn them into a learning roadmap, resume project, and interview plan.'
```

Expected: `github-career-project-planner/`, `github-career-project-planner/SKILL.md`, and `github-career-project-planner/agents/openai.yaml` exist.

- [ ] **Step 4: Run test to verify partial failure**

Run:

```powershell
python tests/test_github_career_project_planner.py
```

Expected: FAIL. The directory and `openai.yaml` tests may pass, but content tests should fail because generated `SKILL.md` is still a template.

### Task 3: 实现 SKILL.md 正文

**Files:**
- Modify: `github-career-project-planner/SKILL.md`

- [ ] **Step 1: Replace SKILL.md with complete skill content**

Replace `github-career-project-planner/SKILL.md` with the Codex `apply_patch` edit tool, or an equivalent structured file-edit tool in another agent runtime. Do not use `echo`, `Set-Content`, `Out-File`, shell redirection, or heredoc-style shell writing for this long Markdown file.

Use this content:

```markdown
---
name: github-career-project-planner
description: Job-targeted GitHub project discovery, repository evaluation, learning roadmap planning, resume project writing, and interview preparation. Use when Codex needs to help a user find suitable GitHub projects for a target job, analyze a job description, evaluate repositories beyond stars, create a project learning roadmap, design second-development tasks, write credible resume bullets, or prepare interview talking points.
---

# GitHub Career Project Planner

## Critical Rules

- Verify current GitHub information with web access before recommending repositories. Repository activity, archived status, stars, forks, releases, and visible maintenance signals change over time.
- If web access is unavailable, use the degraded path: say current GitHub status cannot be verified, ask the user for repository links, README content, or project summaries, and mark repository activity as not real-time verified.
- Do not recommend projects only because they have many stars. Prioritize job fit, learning value, resume value, runnable setup, source structure, and second-development potential.
- Do not fabricate issue resolution rate, PR merge rate, maintainer response time, contributor trend, or community activity. Without GitHub REST API or GraphQL API, only describe visible maintenance signals and uncertainty.
- Distinguish "recommended with risks" from "not recommended and why".
- Keep resume claims credible. Do not present suggested work, expected targets, or future improvements as completed results.
- If source structure cannot be reviewed for a high-priority repository, say so and lower the recommendation confidence.

## Inputs And Conflict Handling

Parse the user's target job, level, constraints, and optional job description.

Support inputs such as:

- Target role: Java backend, frontend, AI application developer, data analyst, DevOps, full-stack, mobile developer.
- Job description or hiring post.
- Experience level: beginner, student, internship, junior, mid-level, career switcher.
- Constraints: preferred language, framework, difficulty, time budget, output language, resume-only output, learning-route-only output, or a single repository link.

Use low-risk defaults when safe:

- If the user provides a job description but no level, infer level from title, years, and required skills.
- If the user says "Java backend campus hire" without stack details, assume Spring Boot, MySQL, Redis, messaging, deployment, and basic engineering practices.
- If the user provides one repository link and asks for resume packaging, evaluate that repository instead of searching for more projects.

Ask one concise question when direction is high-risk ambiguous:

- No target role, no job description, and no repository link.
- Conflicting roles, such as frontend intern and senior backend architect.
- Resume claims are requested but completed work or planned work boundaries are unclear.

When the user's level conflicts with the job description, trust the user's stated level and use the job description as the gap target. Explain the gap between current level and target requirements, then ask whether they want a gap-closing route or short-term resume packaging if needed.

## Search Strategy

Do not search only broad phrases such as `Java Backend Project`, `frontend project`, or `AI project`. These often return learning notes, interview repositories, awesome lists, project collections, and stale examples.

Build precise searches by combining:

- Role technologies: `Spring Boot`, `Redis`, `Kafka`, `React`, `Next.js`, `FastAPI`, `LangChain`, `Kubernetes`.
- Project shapes: `ecommerce`, `blog`, `mall`, `chat`, `workflow`, `admin`, `dashboard`, `rag`, `microservices`, `observability`.
- Runnable signals: `docker-compose`, `demo`, `deployment`, `production-ready`, `starter`, `example app`.
- Exclusions: `awesome`, `interview`, `notes`, `learning notes`, `tutorial-list`, `roadmap`, `八股`, `面试`, `学习笔记`.
- GitHub focus: prefer primary GitHub repository pages over third-party lists, blogs, or ranking pages.

Useful query patterns:

- Java backend intern: `site:github.com spring boot redis docker-compose ecommerce OR mall`
- Java microservices: `site:github.com spring cloud gateway nacos sentinel seata docker-compose`
- Frontend engineer: `site:github.com next.js dashboard auth prisma docker`
- AI application developer: `site:github.com rag fastapi langchain vector database docker`
- DevOps: `site:github.com kubernetes prometheus grafana terraform example`

If result quality is poor, adjust the query and search again instead of forcing weak recommendations.

Before recommending a repository, open the repository page when possible and verify project positioning, tech stack, README quality, and recent visible maintenance signals.

## Repository Evaluation

Evaluate repositories in three priority tiers.

Non-negotiable:

- Match the target role and stack.
- Fit the user's current level, or be decomposable into a realistic learning path.
- Have resume packaging value.
- Allow original second-development work instead of only copying the README.

Important signals:

- README and setup documentation are clear.
- The repository has visible maintenance signals or remains useful despite low activity.
- Architecture and module boundaries are readable.
- The project supports interview discussion.

Bonus signals:

- Visible issue/PR or community maintenance signals are positive, but do not claim exact statistics.
- Deployment, tests, examples, or demo environments exist.
- Recent commits, releases, discussions, or documentation updates provide concrete evidence of activity.
- The project covers multiple target-job skills.

For popular but unsuitable projects, add them under `不推荐及原因` with specific reasons such as too hard for the user's level, framework-source oriented, not runnable, too tutorial-like, or poor short-term resume value.

## Output Contract

Use Chinese section titles by default unless the user asks for another language.

Default full output:

1. `岗位能力拆解`: Target-role skills, project types, and capability keywords.
2. `GitHub 项目推荐`: Repository link, stack, difficulty, recommendation reason, risk notes, learning priority, and a `不推荐及原因` subsection for popular but unsuitable projects.
3. `项目学习路线`: Setup, reading order, core modules, experiments, milestones, and a schedule that scales to the user's time budget. If no time budget is given, state a 3 to 4 week assumption.
4. `二次开发任务`: Concrete second-development tasks by user level. Each recommended project should cover at least two layers from business loop, engineering quality, architecture upgrade, performance and reliability, security and permissions, or deployment and observability.
5. `简历项目描述`: Resume-ready bullets with project background, stack, responsibilities, highlights, and credible quantitative targets or measured outcomes. Expected targets must be labeled as expected target or to-be-measured, not completed fact.
6. `面试准备问题`: Architecture, trade-off, performance, debugging, deployment, security, extension, and `技术选型与踩坑` questions.
7. `下一步行动计划`: A short plan for the next 3 to 7 days.

Narrow Output Modes:

- Project recommendations only: keep `岗位能力拆解` and `GitHub 项目推荐`; omit detailed roadmap and resume bullets.
- Learning route only: keep `GitHub 项目推荐`, `项目学习路线`, `二次开发任务`, and `下一步行动计划`.
- Resume-only: keep a repository summary, verifiable stack, 3 to 5 resume bullets, technical anchors, quantitative baselines, and 5 to 8 interview follow-up questions; omit the full recommendation table and weekly plan.
- Interview-only: keep project summary and `面试准备问题`, grouped by architecture, technical difficulty, trade-off, and pitfalls.
- Single repository link: do not output a multi-project recommendation table; evaluate that repository, then provide learning route, second-development tasks, resume bullets, and interview preparation.

## Second-Development Guidance

Do not stop at generic tasks such as "add login", "add a page", or "improve UI". Propose layered changes based on the role and project type.

Second-development layers:

- Business loop: order state machine, approval flow, payment callback, inventory deduction, permission approval, notifications, import/export.
- Engineering quality: unit tests, integration tests, API docs, error-code conventions, logging conventions, configuration layering, CI checks, Docker Compose one-command startup.
- Architecture upgrade: module boundaries, domain boundaries, cache strategy, async jobs, message queues, rate limiting, circuit breaking, distributed locks, read/write splitting, multi-tenancy.
- Performance and reliability: slow query optimization, cache penetration/breakdown/avalanche handling, load testing, metrics, alerts, tracing, graceful degradation.
- Security and permissions: RBAC, JWT refresh, API authorization, data permissions, audit logs, sensitive data masking, basic security hardening.
- Deployment and observability: Dockerfile, docker-compose, environment templates, health checks, Prometheus, Grafana, OpenTelemetry, log collection.

Each second-development suggestion must include:

- Task goal: why it matters for the target job.
- Technical entry point: modules or components to modify or add.
- Technical anchors: concrete middleware, frameworks, protocols, tools, or components such as Redis, Kafka, RabbitMQ, Elasticsearch, PostgreSQL, MySQL, Docker, Kubernetes, Prometheus, Grafana, OpenTelemetry, Nginx, JWT, OAuth2, RBAC, Spring Security, Celery, BullMQ, Prisma, LangChain, pgvector, or Milvus.
- Deliverable: API, page, deployment URL, load-test report, architecture diagram, README, or demo flow.
- Resume expression: a credible bullet with a quantitative baseline or expected metric range.
- Difficulty: beginner, campus/junior, or mid-level.

Quantitative baseline rules:

- Every technical change must include a measurable indicator, such as response time, throughput, cache hit rate, slow query count, build time, deployment time, error rate, test coverage, resource usage, task latency, or manual operation time.
- Use reasonable ranges, for example: "expected target: reduce product-detail API P95 latency from 300-800ms to 80-200ms".
- If there is no load test or log data, write "expected target" or "measure after completion". Do not present expected targets as completed results.
- Prefer resume bullets in the shape "Designed and implemented X, targeting/measuring Y, supporting Z scenario".
- For beginner projects, use lightweight metrics such as endpoint count, test case count, startup steps reduced from N to M, or manual configuration replaced by one-command startup.

## Source Structure Review

For high-priority repositories that may become deep-learning or resume projects, do not rely only on README. Review the repository skeleton when possible.

Check:

- Entry points such as `main`, `app`, `server`, `src`, `cmd`, `packages`, or framework-specific entry files.
- Dependency and startup files such as `package.json`, `pom.xml`, `build.gradle`, `requirements.txt`, `pyproject.toml`, `Dockerfile`, `docker-compose.yml`, `.env.example`.
- Module boundaries such as controller/service/repository, domain/application/infrastructure, frontend/backend, apps/packages, or services.
- Tests, CI, deployment templates, and environment examples.
- Risks such as giant single-file projects, missing startup docs, stale dependency versions, hard-coded secrets, screenshots without code, or README-only repositories.

If source structure cannot be checked, write "未完成源码骨架核验" and lower the recommendation confidence.

## Anti-Stall Learning Route

Prioritize reducing failure in the startup phase.

Each learning route should include:

- Minimum startup path: run the smallest useful flow first, preferably with Docker Compose, official demo, sample config, or mock data.
- Environment checklist: language version, package manager, database, cache, middleware, environment variables, ports.
- Common blockers: dependency install failure, database initialization failure, missing environment variables, port conflicts, version mismatch, CORS, container startup failure.
- Degraded path: if full startup fails within 1 to 2 hours, inspect module structure, run tests, start a minimal service, mock external dependencies, or switch to a backup project.
- Verification signal: what counts as "running", such as homepage access, login success, core API response, queue consumption, seeded database, or closed demo flow.
- Timebox: set hard limits for startup, reading, second development, and resume packaging.

Timebox defaults:

- Candidate repository evaluation: 10 to 15 minutes per repository.
- Full environment startup: 1 to 2 hours before using the degraded path.
- Single blocker: 30 to 45 minutes before recording the error and changing approach.
- Second-development task: split into 0.5 to 2 day tasks.
- Resume packaging: reserve at least 0.5 day for README, architecture diagram, screenshots, load-test evidence, or validation notes.

## Resume And Interview Guidance

Resume bullets must be credible and defensible.

- Separate completed work from planned improvements.
- Attach technical anchors and quantitative baselines to technical changes.
- Use expected target or to-be-measured wording when there is no evidence yet.
- Avoid vague claims such as "used Redis to improve performance" without scenario, metric, and validation method.

Interview preparation must include `技术选型与踩坑`.

Cover:

- Why this technology.
- What alternatives were considered.
- What cost or complexity it introduces.
- What can go wrong.
- How to validate the improvement.
- How to roll back or degrade gracefully.
```

- [ ] **Step 2: Run tests**

Run:

```powershell
python tests/test_github_career_project_planner.py
```

Expected: PASS for most content tests. If `openai.yaml` was generated without `default_prompt`, Task 4 will fix metadata.

### Task 4: 修正 openai.yaml 元数据

**Files:**
- Modify: `github-career-project-planner/agents/openai.yaml`

- [ ] **Step 1: Ensure openai.yaml uses the schema confirmed in Task 2**

If Task 2 confirmed the local `interface.*` schema, set `github-career-project-planner/agents/openai.yaml` to:

```yaml
interface:
  display_name: "GitHub Career Project Planner"
  short_description: "Find job-targeted GitHub projects"
  default_prompt: "Use $github-career-project-planner to find GitHub projects for my target job and turn them into a learning roadmap, resume project, and interview plan."
```

If Task 2 found a different schema in the local reference file, use that schema instead and update the test regex before running tests.

- [ ] **Step 2: Run tests**

Run:

```powershell
python tests/test_github_career_project_planner.py
```

Expected: PASS.

### Task 5: 运行 skill-creator 校验

**Files:**
- Verify: `github-career-project-planner/SKILL.md`

- [ ] **Step 1: Run quick validation**

Run:

```powershell
python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'github-career-project-planner'
```

Expected: PASS. The validator should accept the skill name, frontmatter, and required fields.

If Windows Python reads files with the default GBK encoding and fails on Chinese section titles, rerun with UTF-8 mode:

```powershell
$env:PYTHONUTF8='1'; python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'github-career-project-planner'
```

- [ ] **Step 2: If quick validation fails, fix only the reported issue**

Use the validator output as the source of truth. Examples:

- If it reports invalid frontmatter keys, remove all frontmatter fields except `name` and `description`.
- If it reports an invalid skill name, keep the folder and frontmatter name exactly `github-career-project-planner`.
- If it reports missing frontmatter delimiters, ensure `SKILL.md` starts with `---` and closes frontmatter with `---` before the Markdown body.

Expected frontmatter shape:

```markdown
---
name: github-career-project-planner
description: Job-targeted GitHub project discovery, repository evaluation, learning roadmap planning, resume project writing, and interview preparation. Use when Codex needs to help a user find suitable GitHub projects for a target job, analyze a job description, evaluate repositories beyond stars, create a project learning roadmap, design second-development tasks, write credible resume bullets, or prepare interview talking points.
---
```

Expected: Re-running `quick_validate.py` passes.

### Task 6: 最终验收

**Files:**
- Verify: `tests/test_github_career_project_planner.py`
- Verify: `github-career-project-planner/SKILL.md`
- Verify: `github-career-project-planner/agents/openai.yaml`

- [ ] **Step 1: Run full local tests**

Run:

```powershell
python tests/test_github_career_project_planner.py
```

Expected: all 8 tests pass.

- [ ] **Step 2: Run skill validation**

Run:

```powershell
python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'github-career-project-planner'
```

Expected: validation passes.

On Windows, use UTF-8 mode if needed:

```powershell
$env:PYTHONUTF8='1'; python 'C:\Users\admin\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'github-career-project-planner'
```

- [ ] **Step 3: Inspect final file tree**

Run:

```powershell
Get-ChildItem -Recurse -File -Exclude '.git' | Where-Object { $_.FullName -notmatch '\\.git\\' } | Select-Object FullName
```

Expected: first-version implementation contains only:

```text
docs/superpowers/specs/2026-06-15-github-career-project-planner-design.md
docs/superpowers/plans/2026-06-15-github-career-project-planner.md  # created before execution
tests/test_github_career_project_planner.py
github-career-project-planner/SKILL.md
github-career-project-planner/agents/openai.yaml
```

No `scripts/`, `references/`, `assets/`, README, changelog, or exporter files should be added for v1.

## Self-Review

- Spec coverage: The plan covers skill files, metadata, TDD tests, search strategy, degraded path, conflict handling, anti-hallucination rules, output contract, narrow output modes, second-development depth, quantitative baselines, source review, anti-stall route, timeboxes, and interview trade-off defense.
- Placeholder scan: No `TBD`, `TODO`, or vague implementation placeholders remain. Each code-writing step includes concrete content.
- Type consistency: Test paths, skill name, headings, metadata fields, and expected file paths are consistent across tasks.
