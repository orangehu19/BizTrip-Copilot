# BizTrip Copilot Demo

本文档记录 BizTrip Copilot 的本地运行流程和可展示场景。所有命令默认在项目根目录执行。

## 1. 环境准备

```powershell
conda activate BizTrip
pip install -r requirements.txt
```

如果只演示 RAG 知识库初始化和离线检索，不需要配置 LLM API key。

如果要演示完整 CLI 对话，需要先配置环境变量：

```powershell
$env:BIZTRIP_API_KEY="your-api-key"
$env:BIZTRIP_MODEL_NAME="deepseek-v4-pro"
$env:BIZTRIP_BASE_URL="https://api.deepseek.com"
```

## 2. 初始化知识库

```powershell
python .claude/skills/ask-question/script/init_knowledge_base.py
```

当前初始化结果：

```text
加载文档：8 个
切分片段：66 个
向量库：Milvus Lite
存储路径：.claude/skills/ask-question/data/rag_knowledge/milvus_lite.db
```

初始化脚本会自动执行 3 个检索样例：

```text
出差住宿标准是多少？
航班延误了怎么办？
机票应该提前多久预订？
```

## 3. 运行离线评测

```powershell
python tests/run_eval.py
```

默认模式只评测 RAG 检索链路，不调用外部 LLM。评测报告会写入：

```text
tests/results/eval_report_latest.md
```

## 4. 启动完整 CLI

```powershell
python cli.py
```

可展示的典型问题：

```text
如何报销差旅费用？需要哪些材料？
航班延误了怎么办？
我偏好住汉庭酒店和如家，座位要靠窗，请记住
我之前说过什么偏好？
我从北京去杭州出差一周，帮我规划行程
杭州下周天气怎么样？
```

## 5. 核心链路说明

RAG 问答链路：

```text
用户问题
→ IntentionAgent 识别为 rag_knowledge
→ OrchestrationAgent 调度 RAGKnowledgeAgent
→ Milvus Lite 语义检索相关政策片段
→ LLM 基于检索结果生成回答
```

行程规划链路：

```text
用户需求
→ IntentionAgent 生成调度计划
→ EventCollectionAgent 抽取出发地、目的地、日期等要素
→ PreferenceAgent / MemoryQueryAgent 补充用户偏好和历史上下文
→ ItineraryPlanningAgent 生成最终行程
```

## 6. 当前边界

- CLI 是当前主要演示入口，尚未提供 Web UI。
- 长期记忆当前使用 JSON 文件存储，Redis/PostgreSQL 属于后续规划。
- 完整意图识别和最终自然语言回答依赖外部 LLM 服务。
- 评测报告中的离线 RAG 指标只代表本地知识库检索效果，不等同于端到端问答准确率。
