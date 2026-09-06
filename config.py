"""
Configuration for the BizTrip Multi-Agent System
"""
import os
from pathlib import Path


def _load_dotenv(dotenv_path: str = ".env") -> None:
    """Load simple KEY=VALUE pairs from .env without adding a dependency."""
    path = Path(__file__).resolve().parent / dotenv_path
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

# LLM Configuration
LLM_CONFIG = {
    "api_key": os.getenv("BIZTRIP_API_KEY") or os.getenv("OPENAI_API_KEY", ""),
    "model_name": os.getenv("BIZTRIP_MODEL_NAME", "deepseek-v4-pro"),
    "base_url": os.getenv("BIZTRIP_BASE_URL") or os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com"),
    "temperature": float(os.getenv("BIZTRIP_TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("BIZTRIP_MAX_TOKENS", "8192")),
}

# System Configuration
SYSTEM_CONFIG = {
    "enable_llm": True,  # Set to True to use LLM (recommended), False for rule-based
    "log_level": "INFO",
    "max_retries": 3,
    "timeout": 60,  # Increased timeout for better stability
}

# RAG 知识库：嵌入模型（本地路径，无需连 HuggingFace）
RAG_CONFIG = {
    "embedding_model": "data/models/bge-small-zh-v1.5",
}

# 连接与可用性：重试、熔断、健康检查
RESILIENCE_CONFIG = {
    "max_retries": 3,              # 单次请求最大重试次数（与 SYSTEM_CONFIG 对齐）
    "retry_base_delay_sec": 1.0,   # 重试退避基数（秒）
    "retry_max_delay_sec": 30.0,   # 重试退避上限（秒）
    "circuit_failure_threshold": 5, # 连续失败多少次后熔断
    "circuit_recovery_timeout_sec": 60.0,  # 熔断后多少秒进入半开
    "circuit_half_open_successes": 2,      # 半开状态下连续成功多少次后关闭
    "health_check_timeout_sec": 10.0,      # 健康检查请求超时（秒）
}
