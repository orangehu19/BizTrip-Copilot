# BizTrip Copilot

一个面向商旅场景的多智能体差旅助手。项目基于 AgentScope 构建 LLM Agent 调度流程，结合本地 RAG 知识库、用户记忆、Skill 插件化加载和 CLI 交互，支持差旅政策问答、偏好管理、历史记忆查询、实时信息查询与行程规划。

> 当前项目定位为可本地运行的个人 AI Agent 项目，用于展示 LLM 应用工程、RAG 检索、多智能体编排和可复现评测能力；不是生产级商旅平台。

## Highlights

- **Multi-Agent Orchestration**: 采用 `IntentionAgent -> OrchestrationAgent -> Skill Agent` 架构，由 LLM 生成结构化执行计划，并动态路由到不同业务 Agent。
- **Plan-and-Execute**: 基于任务优先级调度 Agent，同优先级的信息收集任务通过 `asyncio.gather` 并发执行，依赖结果返回后再生成最终行程方案。
- **Local RAG**: 使用 Milvus Lite + BGE 中文向量模型构建本地差旅知识库，支持政策、报销、预订、FAQ、应急处理等文档检索。
- **Memory System**: 支持短期会话滑窗和 JSON 长期记忆，可保存用户偏好、历史行程和跨会话查询记录。
- **Engineering Reliability**: 为 LLM 调用补充指数退避重试、熔断器、健康检查和环境变量配置，降低外部服务不稳定带来的影响。
- **Reproducible Evaluation**: 提供 30 条场景化 Query 和自动评测脚本，可生成本地评测报告。

## Architecture

```text
User Input
    |
    v
IntentionAgent
    |
    |-- identify user intent
    |-- extract entities
    |-- generate agent schedule
    v
OrchestrationAgent
    |
    |-- load Skill Agents on demand
    |-- execute same-priority tasks concurrently
    |-- merge intermediate results
    v
Skill Agents
    |
    |-- RAGKnowledgeAgent
    |-- ItineraryPlanningAgent
    |-- PreferenceAgent
    |-- MemoryQueryAgent
    |-- InformationQueryAgent
    |-- EventCollectionAgent
    v
Final Response + Memory Update
```

## Features

| Module | Description |
| --- | --- |
| Intent Recognition | 识别行程规划、政策问答、偏好管理、记忆查询、实时信息查询等多类意图 |
| Agent Scheduling | 根据 LLM 输出的 `agent_schedule` 动态调度 Skill Agent |
| RAG QA | 对差旅标准、报销政策、预订指南、FAQ、应急处理等文档进行语义检索 |
| User Memory | 保存用户偏好、历史行程和聊天摘要，支持跨会话查询 |
| CLI Demo | 基于 Rich 构建命令行交互界面 |
| Evaluation | 通过 `tests/run_eval.py` 生成 RAG 检索评测报告 |

## Evaluation

当前默认评测模式为离线 RAG 检索，不调用外部 LLM API。

| Metric | Result |
| --- | --- |
| Knowledge documents | 8 |
| RAG chunks | 66 |
| Evaluation queries | 30 |
| RAG queries executed | 15 |
| RAG passed | 15 / 15 |
| Average latency | 0.016s |

最新报告见 [tests/results/eval_report_latest.md](tests/results/eval_report_latest.md)。

## Quick Start

### 1. Create Environment

```powershell
conda create -n BizTrip python=3.13
conda activate BizTrip
pip install -r requirements.txt
```

### 2. Configure API Key

复制示例配置文件：

```powershell
Copy-Item .env.example .env
```

在 `.env` 中填写自己的 API Key：

```env
BIZTRIP_API_KEY="your_api_key_here"
BIZTRIP_MODEL_NAME=deepseek-v4-pro
BIZTRIP_BASE_URL=https://api.deepseek.com
BIZTRIP_TEMPERATURE=0.7
BIZTRIP_MAX_TOKENS=8192
```

### 3. Initialize Knowledge Base

```powershell
python .claude/skills/ask-question/script/init_knowledge_base.py
```

初始化完成后，本地 Milvus Lite 数据库会生成在：

```text
.claude/skills/ask-question/data/rag_knowledge/
```

### 4. Run Evaluation

```powershell
python tests/run_eval.py
```

完整意图识别评测需要配置 API Key：

```powershell
python tests/run_eval.py --mode full
```

### 5. Start CLI

```powershell
python cli.py
```

可尝试输入：

```text
北京出差住宿标准是多少？
差旅报销需要哪些材料？
我要下周从武汉去上海出差，帮我规划一下
我喜欢靠窗座位，以后帮我记住
我之前说过什么酒店偏好？
```

## Project Structure

```text
BizTrip/
├── agents/                         # IntentionAgent, OrchestrationAgent, lazy registry
├── context/                        # short-term and long-term memory
├── data/
│   ├── memory/                     # local memory files, ignored except .gitkeep
│   └── models/bge-small-zh-v1.5/   # local BGE embedding model
├── docs/                           # demo notes
├── tests/                          # unit tests, eval queries, evaluation runner
├── utils/                          # JSON parsing, circuit breaker, LLM resilience
├── .claude/skills/                 # plugin-style Skill Agents
├── cli.py                          # Rich CLI entrypoint
├── config.py                       # environment-based config
├── config_agentscope.py            # AgentScope initialization
└── requirements.txt
```

