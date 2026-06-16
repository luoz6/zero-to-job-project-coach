# GitHub 项目硬核打分矩阵

## 使用规则

评分用于比较和解释，不用于制造虚假的精确性。所有分数必须基于 README、源码结构、可见提交、release、issue 页面、demo、依赖配置等可见证据；无法核验时降低置信度并标注“未实时核实”。

阶段匹配判断需结合 role_templates.md 的底层基线。

## 评分步骤

1. 先判断是否命中一票否决；命中则直接排除，不进入打分。
2. 再判断岗位匹配和阶段匹配，先看它是否适合当前用户，而不是先看 star。
3. 再评估工程规范度与技术栈含金量，确认是否有真实可运行骨架。
4. 再评估二次开发空间，确认是否存在可讲、可改、可验证的技术切入点。
5. 最后补可见维护信号，作为辅助加减分而不是核心决定因素。

以上每一步，如果证据不足，降低置信度或下调证据等级，不要乱补分或假装核验过。

## 满分 100 分

- 工程规范度 25 分：模块结构清晰、依赖配置完整、README 启动步骤可执行、Docker 或脚本支持、测试/CI/部署材料可见。
- 技术栈含金量 25 分：覆盖目标岗位的高频企业技术栈，技术选型能服务业务闭环，而不是堆概念。
- 学习价值与阶段匹配 20 分：适合用户当前水平，可拆成学习路线，能在时间预算内形成展示版本，能支撑面试讲解。
- 二次开发空间 20 分：存在可改造模块、性能瓶颈、业务扩展点、架构治理点或可量化优化目标。
- 可见维护信号 10 分：近期 commit、release、issue 回复、文档更新或社区使用信号可见。

## 总分与结论映射基准

- ≥ 85 分：强烈推荐，作为核心项目库优先使用。
- 70 - 84 分：推荐但有风险，必须明确指出短板或降级路线。
- < 70 分：不推荐，仅可作为源码参考，不得作为主推简历项目。

## 证据等级修正规则

- 证据等级为 C 时，即使分数 ≥ 85，也不得标注为“强烈推荐”，结论最多只能是“推荐但有风险”。
- 证据等级为 B+ 或 A 时，总分映射结论正常使用。

## 一票否决

- 长期未维护且无法运行。
- 缺乏核心源码。
- 完全没有 README 启动说明。
- 只有学习笔记、面试题、awesome list 或项目合集。
- 明显超出用户当前阶段且无法拆成可执行学习路线。
- 项目内容主要是课程代码搬运，缺少独立业务闭环。

## 禁止高分场景

以下场景不是一票否决，可以继续评估，也可能进入推荐列表，但总分必须被压低，通常不应作为最高优先级推荐：

- README 很完整，但源码结构混乱或关键模块边界不清。
- 技术栈豪华，但业务闭环不明确，难以形成可讲项目。
- 项目可以运行，但二次开发空间很弱，只适合照着演示，不适合做简历亮点。
- 项目偏难，但可以拆成学习路线；这种情况可以推荐，但必须附降级学习路线和风险提示。

禁止高分场景不是一票否决。它的含义是“可以推荐，但不能高分通过”。

## 二次开发空间特征锚点

- 加分特征：README 中提到 TODO 列表；存在简单的本地缓存，容易替换为 Redis；存在同步调用，容易改造为 MQ 异步；有基础的用户表但缺权限控制，容易外挂 JWT 或权限系统。
- 扣分特征：高度封装的脚手架（原版若依等）；各种底层组件硬编码耦合；缺乏独立业务域；纯技术 Demo。
- 识别到可改造点后，必须继续翻译成简历价值：写清楚“改了什么、为什么改、带来什么业务收益或指标预期”，不要只停留在特征描述。

## 不推荐及原因

热门但不适合的仓库必须明确标注为“不推荐”，并说明原因。典型原因包括：star 很高但只是 awesome list、学习笔记或面试题；技术栈过旧；启动链路缺失；对新手阶段明显过难；缺少可二次开发空间；无法形成可信简历项目。

## 阶段匹配扣分锚点

- 用户只会基础语法，项目包含微服务、Kafka/RocketMQ、分布式事务、Kubernetes 等多组件链路：学习价值与阶段匹配至少扣 15 分，并触发降级学习路线。
- 用户只会框架 CRUD，项目要求理解框架源码、编译器、数据库内核或复杂分布式一致性：学习价值与阶段匹配至少扣 10 分。
- 用户时间预算少于 2 周，项目无法在 1 到 2 天内跑通最小闭环：学习价值与阶段匹配至少扣 10 分。
- 项目技术栈豪华但业务闭环不清、无法形成可讲项目：学习价值与阶段匹配不得高于 10 分。
- 项目较难但可拆成最小启动、模块阅读、单点二开和可验收成果：可以保留推荐，但必须输出降级学习路线。

## 证据等级

- A：已查看 README、源码结构、依赖配置以及可见维护信号，关键证据较完整，且核心证据栏有具体文件路径或 URL。
- B+：已查看关键页面，但查了没找到关键证据，例如源码结构混乱、启动入口不清、模块边界无法充分确认，且有具体路径或 URL 说明查找过的位置。
- B：已查看仓库主页和 README，但未深入核验源码结构或依赖配置；如果没有具体文件路径或 URL，必须降级为 B。
- C：未实时核实，仅基于用户描述、搜索摘要或不完整页面信息进行判断。

需要明确区分“没去查”和“查了没找到”。B+ 表示查了但证据不足，B 表示只做了浅层核验，C 表示没有实时核验。
如果仅使用了 Web Search 的摘要或 snippet，没有打开更深层页面，只能是 C 级或 B 级。
如果要给 A 级或 B+ 级，必须在“核心证据”栏附上具体的文件路径或 URL。
如果没有具体路径或 URL，强制降级为 B。

## 评分输出模板

先输出结论总览表，再输出分项评分表，最后输出核心证据、主要风险和下一步建议。不得压成单段文本。

### 结论总览表

| 字段 | 内容 |
| --- | --- |
| 项目名 / 仓库链接 |  |
| 总分 |  |
| 证据等级 |  |
| 结论 | 推荐 / 推荐但有风险 / 不推荐 |

### 分项评分表

| 评分维度 | 得分 | 证据摘要 | 扣分原因 |
| --- | --- | --- | --- |
| 工程规范度 |  |  |  |
| 技术栈含金量 |  |  |  |
| 学习价值与阶段匹配 |  |  |  |
| 二次开发空间 |  |  |  |
| 可见维护信号 |  |  |  |

每一行都必须填写扣分原因；如果没有明显问题，也要写“无明显扣分项”。

### 核心证据

- 

### 主要风险

- 

### 下一步建议

- 

核心证据、主要风险和下一步建议必须逐条换行，不得合并成一整段。

## 评分输出示例

### 结论总览表

| 字段 | 内容 |
| --- | --- |
| 项目名 / 仓库链接 | `spring-boot-cache-mq-demo` / `https://github.com/example/spring-boot-cache-mq-demo` |
| 总分 | 78 |
| 证据等级 | B |
| 结论 | 推荐但有风险 |

### 分项评分表

| 评分维度 | 得分 | 证据摘要 | 扣分原因 |
| --- | --- | --- | --- |
| 工程规范度 | 19/25 | README 提供本地启动步骤；可见 `docker-compose.yml`、`pom.xml` 和服务模块目录。 | 部分环境变量说明偏少，测试说明不完整。 |
| 技术栈含金量 | 20/25 | 具备 Spring Boot + Redis + RocketMQ + docker-compose，贴近常见中间件链路。 | 缺少链路观测或限流治理组件。 |
| 学习价值与阶段匹配 | 16/20 | 业务闭环清晰，适合从缓存一致性和异步订单链路切入。 | 对新手仍有中间件启动成本，需要降级路线。 |
| 二次开发空间 | 15/20 | 可从本地缓存升级为 Redis、多同步调用改为 MQ 异步、补权限控制。 | 源码扩展点尚未做深层核验。 |
| 可见维护信号 | 8/10 | 仓库主页和 README 可见最近更新痕迹。 | 未进一步核验更深层维护信号。 |

### 核心证据

- README 给出了服务启动顺序和本地依赖说明。
- 可见 `docker-compose.yml`，说明 Redis、MQ 一类依赖具备本地编排信号。
- 模块命名显示有订单、缓存或消息链路，具备二次开发切入点。

### 主要风险

- 目前只有浅层核验，源码模块边界和关键扩展点还没有做深查。
- 对零基础用户来说，中间件依赖偏多，可能需要先走最小启动路线。
- 如果后续发现仓库更像脚手架拼装，推荐优先级应下调。

### 下一步建议

- 先确认项目的最小启动路径，比如 Docker Compose 一键启动或本地启动步骤。
- 验证核心接口是否跑通，比如首页、登录、订单查询等 3-5 个关键接口。
- 优先把“本地缓存 -> Redis 缓存”或“同步调用 -> RocketMQ 异步链路”做成第一阶段改造。
- 输出时同步写明简历价值，例如延迟预期、吞吐预期或故障隔离收益，但未实测前必须标注“完成后待验证”。

## 反幻觉边界

- 不得编造 issue 解决率、PR 合并率、维护者响应时间、贡献者趋势或社区活跃度。
- 可以说“从页面可见信号看维护较活跃/偏弱”，但必须说明依据。
- 如果没有直接打开仓库页面或无法联网，只能写“未实时核实”，不能假装检查过。
- 不得把 GitHub star 当作核心推荐理由，只能作为辅助热度信号。

## 降级学习路线

当项目总分高但阶段匹配不足时，不要直接放弃；先判断是否能拆成路线：

- 第 1 步：只跑通最小启动路径。
- 第 2 步：阅读入口文件、依赖配置和核心模块边界。
- 第 3 步：选择一个低风险模块做业务闭环改造。
- 第 4 步：补充测试、日志、README 和可展示截图。
- 第 5 步：再选择一个技术锚点升级为简历亮点。

## 搜索策略

搜索目标是找到“可运行、可二次开发、能转化为简历”的项目，而不是 star 最高的列表。

- 优先使用精准信号组合：岗位关键词 + 技术栈 + 启动/部署信号 + 业务场景。
- 示例查询：`site:github.com spring boot redis docker-compose ecommerce OR mall`。
- Java 后端示例：`site:github.com spring boot redis rocketmq docker-compose order system`。
- AI 应用示例：`site:github.com RAG langchain vector database docker chatbot`。
- 前端示例：`site:github.com react dashboard permission vite api`。
- 优先寻找中等体量项目，快速信号是 3-15 个核心模块/服务目录，非单文件，非 50+ 微服务的巨型 monorepo；避开单文件玩具、纯教程仓库和过于庞大的基础设施巨兽。
- 宽泛查询只用于扩展候选池，例如 `Java backend project`；不得直接用宽泛查询结果做最终推荐。

**排除关键词（搜索时必须携带负面词缀 `-`）**：
- 非项目内容：`-awesome -interview -notes -学习笔记 -面试题 -教程 -course`
- 非独立项目：`-demo -collection -template -starter -boilerplate -脚手架`
- 学生/培训作业：`-毕业设计 -课程设计 -培训作业 -后台管理系统`
- 不可二次开发：`-ruoyi -jeecg` 等高度封装脚手架

**如果候选结果质量差，调整查询后重新搜索，不要硬凑推荐。**
- 调整方向：增加业务场景词、换同义技术栈、去掉过窄的细分关键词。

**仓库评估动作盒 (Action Box)**：
大模型在评估时，每个目标最多允许执行以下动作，超过动作上限仍证据不足，立即降低该仓库置信度或放弃：
- **全局发现**：最多 2 轮主查询/回退查询。
- **单点深挖**：针对某个具体候选仓库，最多 1 轮定向补充查询（用于核验配置文件或特定中间件）。

## 严格查询配方库 (Query Recipes)

大模型在调用搜索工具时，必须直接套用或拼接以下配方，严禁使用自然语言短句。必须在所有全局搜索末尾携带黑名单词簇。

### 1. Java 后端配方

- 主查询 (全局发现)：`site:github.com "spring boot" (redis OR rocketmq) docker-compose (order OR mall OR payment) -awesome -interview -tutorial -ruoyi -毕业设计`
- 回退查询 (放宽业务域)：`site:github.com "spring boot" redis docker-compose (system OR platform) -awesome -course -脚手架`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] pom.xml rocketmq`

### 2. 前端 / 全栈配方

- 主查询 (全局发现)：`site:github.com (react OR vue OR vue3) (vite OR next.js) (admin OR dashboard OR saas) permission -awesome -notes -template -course`
- 全栈回退查询 (放宽业务域)：`site:github.com (react OR vue) (express OR nest OR fastapi OR gin) fullstack docker-compose -awesome -tutorial`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] package.json prisma`

### 3. AI 应用开发配方

- 主查询 (全局发现)：`site:github.com (rag OR llm) langchain (milvus OR chroma OR weaviate) chatbot docker -awesome -learning -tutorial`
- 回退查询 (放宽业务域)：`site:github.com rag (retrieval OR embedding) vector database python app -awesome -notes -demo`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] requirements.txt langchain`

### 4. Go 后端配方

- 主查询 (全局发现)：`site:github.com (gin OR hertz) (go-zero OR grpc) (redis OR kafka OR rocketmq) docker-compose -awesome -interview -tutorial`
- 回退查询 (放宽业务域)：`site:github.com go backend (gin OR hertz) fullstack -awesome -course -starter`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] go.mod redis`

### 5. DevOps 配方

- 主查询 (全局发现)：`site:github.com docker kubernetes prometheus grafana jenkins -awesome -notes -tutorial`
- 回退查询 (放宽业务域)：`site:github.com github actions docker-compose deploy monitor -awesome -starter -boilerplate`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] docker-compose.yml prometheus`

### 6. 数据分析配方

- 主查询 (全局发现)：`site:github.com python sql pandas streamlit dashboard -awesome -course -tutorial`
- 回退查询 (放宽业务域)：`site:github.com jupyter notebook pandas analytics -awesome -notes -demo`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] requirements.txt pandas`

### 7. 移动端开发配方

- 主查询 (全局发现)：`site:github.com (android OR ios OR flutter OR react native) (sqlite OR realm OR supabase) app -awesome -tutorial -template`
- 回退查询 (放宽业务域)：`site:github.com flutter mobile app offline cache -awesome -notes -starter`
- 单点深挖 (定向核验某个仓库)：`site:github.com/[开发者]/[仓库名] pubspec.yaml flutter`

注：如果大模型当前环境调用的是 GitHub 原生搜索工具而非 Google/Bing，排除词应在查询末尾集中改写为 `NOT keyword` 形式，并避免把 `site:` 与 GitHub 专有搜索语法混写在同一条查询里。
