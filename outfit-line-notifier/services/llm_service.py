import logging

import requests

from config import AppConfig

logger = logging.getLogger(__name__)


def call_ollama(prompt: str) -> str | None:
    """OllamaのローカルLLMにプロンプトを送信してレスポンスを返す。失敗時はNoneを返す。"""
    url = f"{AppConfig.OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": AppConfig.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.ConnectionError:
        logger.error(
            "Ollamaに接続できません。ollama serve が起動しているか確認してください。"
        )
        return None
    except requests.Timeout:
        logger.error("Ollamaへのリクエストがタイムアウトしました。")
        return None
    except requests.RequestException as e:
        logger.error("Ollama呼び出し失敗: %s", e)
        return None
