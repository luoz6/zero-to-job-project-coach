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
3. `项目学习路线`: Setup, reading order, core modules, experiments, milestones, and a schedule that scales to the user's time budget. Always scale the schedule to the user's time budget. If no time budget is given, state a 3 to 4 week assumption.
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
