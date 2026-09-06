#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scenario evaluation for BizTrip Copilot.

Default mode evaluates local RAG retrieval only and does not call an LLM.
Use --mode full to evaluate LLM-based intent recognition when API config is ready.
"""
import argparse
import asyncio
import importlib.util
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from statistics import mean

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
QUERIES_PATH = PROJECT_ROOT / "tests" / "eval_queries.json"
RESULTS_DIR = PROJECT_ROOT / "tests" / "results"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def load_queries() -> list[dict]:
    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_rag_agent_class():
    agent_path = PROJECT_ROOT / ".claude" / "skills" / "ask-question" / "script" / "agent.py"
    spec = importlib.util.spec_from_file_location("biztrip_rag_agent", agent_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load RAG agent from {agent_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.RAGKnowledgeAgent


def format_seconds(value: float) -> str:
    return f"{value:.3f}s"


def keyword_matches(text: str, expected_keywords: list[str]) -> list[str]:
    return [keyword for keyword in expected_keywords if keyword and keyword in text]


def evaluate_rag(queries: list[dict]) -> dict:
    RAGKnowledgeAgent = load_rag_agent_class()
    agent = RAGKnowledgeAgent(model=None)
    rows = []

    try:
        for item in queries:
            if item.get("expected_intent") != "rag_knowledge":
                rows.append({
                    "id": item["id"],
                    "category": item["category"],
                    "query": item["query"],
                    "expected_intent": item["expected_intent"],
                    "status": "skipped",
                    "latency_sec": None,
                    "matched_keywords": [],
                    "top_titles": [],
                    "note": "默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。",
                })
                continue

            start = time.perf_counter()
            docs = agent.search_knowledge(item["query"], top_k=3)
            latency = time.perf_counter() - start

            combined_text = "\n".join(
                [
                    doc.get("content", "")
                    + "\n"
                    + json.dumps(doc.get("metadata", {}), ensure_ascii=False)
                    for doc in docs
                ]
            )
            matched = keyword_matches(combined_text, item.get("expected_keywords", []))
            top_titles = [
                doc.get("metadata", {}).get("title", "Unknown")
                for doc in docs[:3]
            ]

            rows.append({
                "id": item["id"],
                "category": item["category"],
                "query": item["query"],
                "expected_intent": item["expected_intent"],
                "status": "pass" if docs and matched else "fail",
                "latency_sec": latency,
                "matched_keywords": matched,
                "top_titles": top_titles,
                "note": "",
            })
    finally:
        agent.close()

    return build_summary(rows, mode="rag")


async def evaluate_full(queries: list[dict]) -> dict:
    from agentscope.message import Msg
    from agentscope.model import OpenAIChatModel
    from config import LLM_CONFIG
    from config_agentscope import init_agentscope
    from agents.intention_agent import IntentionAgent

    if not LLM_CONFIG.get("api_key"):
        raise RuntimeError(
            "BIZTRIP_API_KEY is not configured. Set it before running --mode full."
        )

    init_agentscope()
    model = OpenAIChatModel(
        model_name=LLM_CONFIG["model_name"],
        api_key=LLM_CONFIG["api_key"],
        client_kwargs={
            "base_url": LLM_CONFIG["base_url"],
            "timeout": 60,
        },
        generate_kwargs={
            "temperature": LLM_CONFIG.get("temperature", 0.7),
            "max_tokens": LLM_CONFIG.get("max_tokens", 2000),
        },
    )
    agent = IntentionAgent(name="IntentionAgent", model=model)

    rows = []
    for item in queries:
        start = time.perf_counter()
        result = await agent.reply([Msg(name="user", content=item["query"], role="user")])
        latency = time.perf_counter() - start

        try:
            data = json.loads(result.content)
        except json.JSONDecodeError:
            data = {}

        recognized = [
            intent.get("type", "")
            for intent in data.get("intents", [])
            if isinstance(intent, dict)
        ]
        expected = item.get("expected_intent")

        rows.append({
            "id": item["id"],
            "category": item["category"],
            "query": item["query"],
            "expected_intent": expected,
            "status": "pass" if expected in recognized else "fail",
            "latency_sec": latency,
            "recognized_intents": recognized,
            "matched_keywords": [],
            "top_titles": [],
            "note": "",
        })

    return build_summary(rows, mode="full")


def build_summary(rows: list[dict], mode: str) -> dict:
    executed = [row for row in rows if row["status"] != "skipped"]
    passed = [row for row in executed if row["status"] == "pass"]
    failed = [row for row in executed if row["status"] == "fail"]
    latencies = [
        row["latency_sec"]
        for row in executed
        if isinstance(row.get("latency_sec"), (int, float))
    ]
    by_category = {}
    for row in rows:
        cat = row["category"]
        bucket = by_category.setdefault(cat, {"total": 0, "executed": 0, "pass": 0, "fail": 0, "skipped": 0})
        bucket["total"] += 1
        bucket[row["status"]] += 1
        if row["status"] != "skipped":
            bucket["executed"] += 1

    return {
        "mode": mode,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(rows),
        "executed": len(executed),
        "passed": len(passed),
        "failed": len(failed),
        "skipped": len(rows) - len(executed),
        "pass_rate": (len(passed) / len(executed)) if executed else 0,
        "avg_latency_sec": mean(latencies) if latencies else 0,
        "max_latency_sec": max(latencies) if latencies else 0,
        "by_category": by_category,
        "rows": rows,
    }


def write_report(summary: dict) -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = RESULTS_DIR / f"eval_report_{summary['mode']}_{timestamp}.md"
    latest_path = RESULTS_DIR / "eval_report_latest.md"

    content = render_report(summary)
    for path in (report_path, latest_path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return report_path


def render_report(summary: dict) -> str:
    lines = [
        "# BizTrip Copilot Evaluation Report",
        "",
        f"- 生成时间: {summary['generated_at']}",
        f"- 评测模式: {summary['mode']}",
        f"- Query 总数: {summary['total']}",
        f"- 实际执行: {summary['executed']}",
        f"- 通过: {summary['passed']}",
        f"- 失败: {summary['failed']}",
        f"- 跳过: {summary['skipped']}",
        f"- 通过率: {summary['pass_rate']:.1%}",
        f"- 平均耗时: {format_seconds(summary['avg_latency_sec'])}",
        f"- 最大耗时: {format_seconds(summary['max_latency_sec'])}",
        "",
        "## 分类统计",
        "",
        "| 分类 | 总数 | 执行 | 通过 | 失败 | 跳过 |",
        "|------|------|------|------|------|------|",
    ]

    for category, stats in sorted(summary["by_category"].items()):
        lines.append(
            f"| {category} | {stats['total']} | {stats['executed']} | {stats['pass']} | {stats['fail']} | {stats['skipped']} |"
        )

    lines.extend([
        "",
        "## 明细",
        "",
        "| ID | Query | 预期意图 | 状态 | 耗时 | 命中关键词 / 识别意图 | Top 结果 |",
        "|----|-------|----------|------|------|----------------------|----------|",
    ])

    for row in summary["rows"]:
        latency = "-" if row["latency_sec"] is None else format_seconds(row["latency_sec"])
        evidence = ", ".join(row.get("matched_keywords") or row.get("recognized_intents") or [])
        if not evidence:
            evidence = row.get("note", "")
        titles = "<br>".join(row.get("top_titles", []))
        query = row["query"].replace("|", "\\|")
        evidence = evidence.replace("|", "\\|")
        titles = titles.replace("|", "\\|")
        lines.append(
            f"| {row['id']} | {query} | {row['expected_intent']} | {row['status']} | {latency} | {evidence} | {titles} |"
        )

    if summary["mode"] == "rag":
        lines.extend([
            "",
            "## 说明",
            "",
            "默认 RAG 模式只评测本地知识库检索链路，不调用外部 LLM。非 RAG Query 会被记录为 skipped；配置 API key 后可使用 `python tests/run_eval.py --mode full` 评测意图识别。",
        ])

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=["rag", "full"],
        default="rag",
        help="rag: local RAG retrieval only; full: LLM intent recognition",
    )
    args = parser.parse_args()

    queries = load_queries()
    if args.mode == "rag":
        summary = evaluate_rag(queries)
    else:
        summary = asyncio.run(evaluate_full(queries))

    report_path = write_report(summary)
    print(f"Report written: {report_path}")
    print(
        f"Executed {summary['executed']}/{summary['total']}, "
        f"passed {summary['passed']}, failed {summary['failed']}, "
        f"avg latency {format_seconds(summary['avg_latency_sec'])}"
    )


if __name__ == "__main__":
    main()
