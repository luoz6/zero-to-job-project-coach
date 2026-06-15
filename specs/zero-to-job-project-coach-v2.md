# Zero To Job Project Coach v2 设计规格

## 目标

将 `zero-to-job-project-coach` 从“项目推荐与简历包装 skill”升级为“主控引擎 + 外挂知识矩阵”的求职推进型 skill。v2 要帮助新手从当前水平出发，经过阶段诊断、岗位拆解、GitHub 项目选型、二次开发验收、简历转化、面试拷问和投递复盘，形成可执行的求职闭环。

## 非目标

- 不承诺 offer、高薪、保过面试或保证录用。
- 不实现 GitHub API 客户端、爬虫、自动投递器或简历导出器。
- 不把五个 reference 写成大型百科；第一版每个 reference 保持可读、可维护，优先覆盖高频岗位和高价值规则。
- 不提交或使用 `docs/superpowers/` 下的规划文件。

## 当前问题

当前 `SKILL.md` 已覆盖搜索、评估、二次开发、简历和面试，但存在三个结构性问题：

- 主文件承载过多知识细节，后续扩展会变长并稀释关键规则。
- “从 0 到找工作”的阶段推进感不足，用户容易跳过项目选择、实操验收和面试防守。
- 岗位路径、项目评分、二开蓝图、简历案例和面试题库没有独立知识库，难以维护和测试。

## 目标文件结构

第一版 v2 创建或修改以下文件：

```text
zero-to-job-project-coach/
  SKILL.md
  agents/
    openai.yaml
  references/
    role_templates.md
    github_scoring_matrix.md
    secondary_dev_blueprints.md
    resume_benchmarks.md
    job_execution_playbook.md
tests/
  test_zero_to_job_project_coach.py
specs/
  zero-to-job-project-coach-v2.md
```

`SKILL.md` 作为主控引擎，只保留调度逻辑、阶段状态机、关键红线和 reference 读取规则。五个 reference 文件承载细节知识。

## 五大 reference 知识库

### `references/role_templates.md`

定位：岗位路径与里程碑验收库。

必须包含：

- 至少覆盖 Java 后端、前端、AI 应用开发、数据分析、DevOps 五类岗位。
- 每个岗位包含：底层基线、进阶能力、推荐项目类型、最低简历项目标准、里程碑验收问题。
- Java 后端必须覆盖 Spring Boot、MyBatis、AOP、Redis、消息队列、服务治理或部署工程化。
- AI 应用开发必须覆盖 RAG、LangChain 或同类编排框架、向量数据库、TextSplitter 对检索效果的影响。

### `references/github_scoring_matrix.md`

定位：GitHub 项目硬核打分矩阵。

必须包含满分 100 分规则：

- 工程规范度 30 分。
- 技术栈含金量 30 分。
- 二次开发空间 25 分。
- 可见维护信号 15 分。

必须包含一票否决规则：

- 长期未维护且无法运行。
- 缺乏核心源码。
- 完全没有 README 启动说明。
- 只有学习笔记、面试题、awesome list 或项目合集。

必须要求不要编造精确 issue/PR 统计；只能使用可见维护信号和不确定性描述。

### `references/secondary_dev_blueprints.md`

定位：高阶二次开发蓝图库。

必须包含三级改造：

- Level 1 业务闭环：状态机、支付回调、权限审批、导入导出、通知。
- Level 2 架构与高并发：Caffeine + Redis 多级缓存、消息队列解耦、Canal binlog 同步、异步任务、限流熔断。
- Level 3 治理与性能：动态线程池、压测基准、Prometheus/Grafana、OpenTelemetry、灰度或降级方案。

每个蓝图必须包含：适用场景、技术锚点、改造步骤、可交付物、验收问题、简历表达模板。

### `references/resume_benchmarks.md`

定位：简历标杆与 few-shot 案例库。

必须包含：

- STAR 法则说明。
- 低效表达与高阶表达对比。
- 至少覆盖 Java 后端、前端、AI 应用开发三类项目 bullet。
- 量化指标规则：没有实测数据时必须写“预期目标”或“完成后待实测”，不得写成已完成结果。
- 简历防守清单：每条 bullet 必须能回答场景、技术选型、指标来源、踩坑和回滚方案。

### `references/job_execution_playbook.md`

定位：求职闭环与面试高压题库。

必须包含：

- 面试追问题库，重点覆盖技术选型与踩坑。
- 投递执行表字段：日期、岗位、公司分层、简历版本、投递渠道、反馈、被问问题、盲区、下一步修正。
- 1 到 2 周投递节奏模板。
- 面试复盘机制：每次面试后沉淀高频问题、简历风险点和补强任务。

## SKILL.md 主控引擎

`SKILL.md` 必须瘦身为调度器，包含以下核心章节：

- `## 关键规则`
- `## Reference 调度规则`
- `## 三阶段解锁工作流`
- `## Phase 1：诊断、拆解与选型定调`
- `## Phase 2：硬核开模与验收标准`
- `## Phase 3：交付转化与求职冲刺`
- `## 降级路径`
- `## 输出控制`

### Reference 调度规则

必须明确什么时候读取哪个 reference：

- 未明确岗位或需要岗位能力拆解时，读取 `references/role_templates.md`。
- 需要搜索、筛选或比较 GitHub 项目时，读取 `references/github_scoring_matrix.md`。
- 用户已选择项目或需要二次开发方案时，读取 `references/secondary_dev_blueprints.md`。
- 用户需要简历 bullet 或项目包装时，读取 `references/resume_benchmarks.md`。
- 用户进入面试准备、投递计划或复盘时，读取 `references/job_execution_playbook.md`。

### Phase 1：诊断、拆解与选型定调

目标：定位用户阶段，确定岗位路径，选出 2 到 3 个高优先级项目。

必须包含：

- 阶段探针诊断：如果用户没说明现状，提出 2 到 3 个核心问题。
- 读取 `role_templates.md` 对齐岗位技术底线和里程碑。
- 联网搜索 GitHub 项目；无法联网时让用户提供候选仓库链接或 README。
- 读取 `github_scoring_matrix.md` 给候选仓库打分。
- 输出项目分数、优势、风险、适合人群和推荐优先级。
- 阶段卡点：默认在 Phase 1 结束后停顿，等待用户确认选择项目后再进入 Phase 2。

### Phase 2：硬核开模与验收标准

目标：让用户把选定项目做成可讲、可写、可验收的作品。

必须包含：

- 防卡壳启动路线：最小启动路径、环境检查、常见卡点、降级路径、验收信号、时间盒。
- 读取 `secondary_dev_blueprints.md`，为选定项目定制 2 到 3 个二次开发任务。
- 每个任务包含技术锚点、改造步骤、预期交付物、预期指标和验收问题。
- 阶段卡点：要求用户完成改造或至少回答验收问题后，再进入 Phase 3。
- 允许用户显式要求“先预览 Phase 3”，但必须标注未完成实操带来的简历风险。

### Phase 3：交付转化与求职冲刺

目标：把完成的项目成果转化为简历、面试表达和投递执行。

必须包含：

- 读取 `resume_benchmarks.md`，生成符合 STAR 和量化规则的简历 bullet。
- 区分已完成成果、预期目标和待实测指标。
- 读取 `job_execution_playbook.md`，生成 3 到 5 轮高压追问。
- 输出 1 到 2 周投递行动计划和复盘表。

## 输出契约

默认按阶段输出，不一次性输出所有阶段。

Phase 1 默认输出：

- `当前阶段诊断`
- `目标岗位拆解`
- `GitHub 项目候选与评分`
- `推荐项目排序`
- `Phase 1 卡点：请选择一个项目`

Phase 2 默认输出：

- `防卡壳启动路线`
- `二次开发蓝图`
- `技术锚点与交付物`
- `验收问题`
- `Phase 2 卡点：完成改造或回答验收问题`

Phase 3 默认输出：

- `简历项目描述`
- `面试高压追问`
- `投递行动计划`
- `复盘表`

窄输出规则：

- 用户只要“项目推荐”：只执行 Phase 1。
- 用户只要“二次开发”：要求先确认项目，然后执行 Phase 2。
- 用户只要“简历”：如果没有项目成果，先提示风险；可生成草稿但必须标注待验证。
- 用户只要“面试”：读取 `job_execution_playbook.md`，围绕项目成果追问。

## 测试策略

实现必须使用 TDD：

1. 先更新测试，验证 v2 结构缺失时失败。
2. 创建五个 reference 文件的最小内容，让文件存在性测试通过。
3. 更新 `SKILL.md` 为主控引擎，让调度规则和三阶段工作流测试通过。
4. 补足 reference 内容，让关键知识点测试通过。
5. 运行 skill 校验，并同步到 Codex skill 库。

测试必须验证：

- `zero-to-job-project-coach/references/` 存在。
- 五个 reference 文件存在。
- `SKILL.md` 引用五个 reference 文件。
- `SKILL.md` 包含 `Reference 调度规则` 和 `三阶段解锁工作流`。
- `SKILL.md` 包含 Phase 1、Phase 2、Phase 3。
- `SKILL.md` 明确阶段卡点和允许预览 Phase 3 的风险提示。
- `role_templates.md` 覆盖 Java 后端、前端、AI 应用开发、数据分析、DevOps。
- `github_scoring_matrix.md` 包含 100 分评分矩阵和一票否决规则。
- `secondary_dev_blueprints.md` 包含 Level 1、Level 2、Level 3 改造蓝图。
- `resume_benchmarks.md` 包含 STAR、低效表达、高阶表达和量化指标规则。
- `job_execution_playbook.md` 包含高压追问、投递执行表和 1 到 2 周投递节奏。
- 现有测试中关于不编造 GitHub 精确统计、可信简历、技术选型与踩坑、防卡壳路线的核心约束不能回退。

## 验收标准

v2 完成条件：

- 所有测试通过。
- `quick_validate.py` 校验通过。
- `SKILL.md` 主体比当前版本更像调度器，而不是知识百科。
- 五个 reference 文件内容可独立维护。
- Codex skill 库中的 `zero-to-job-project-coach` 已同步更新。
- 不提交 `docs/superpowers/`。
- 不提交 `.idea/`。

## 风险与缓解

风险：reference 文件过大，导致维护困难。  
缓解：第一版只写高频岗位和高价值案例，后续增量扩展。

风险：阶段卡点让用户觉得流程太慢。  
缓解：允许用户显式要求预览后续阶段，但必须提示未实操的简历风险。

风险：评分矩阵看似精确但依据不足。  
缓解：分数必须基于可见证据；没有证据时降低置信度，不编造 issue/PR 精确统计。

风险：简历 bullet 过度包装。  
缓解：强制区分已完成、预期目标和待实测指标。

## 自检

本规格没有占位项。范围聚焦在一个 skill 的 v2 架构升级，文件边界清晰，TDD 验收项覆盖主控引擎、五个 reference、阶段卡点、降级路径和同步要求。
