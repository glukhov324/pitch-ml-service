from typing import List, Dict
import requests
import json
import time

from src.config import settings



def call_openrouter(messages: List[Dict[str, str]],
                    model: str = settings.MODEL_ID,
                    temperature: float = settings.TEMPERATURE,
                    max_tokens: int = settings.MAX_TOKENS,
                    retries: int = settings.OPENROUTER_RETRIES,
                    timeout: int = settings.OPENROUTER_TIMEOUT) -> str:
    """Устойчивый вызов OpenRouter: ретраи на 429/5xx, именованные аргументы поддерживаются."""

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # опционально (участвуют в рейтингах на openrouter.ai):
        "HTTP-Referer": "http://localhost",
        "X-Title": "Speech-Coach-RU",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    for attempt in range(retries + 1):
        
        resp = requests.post(settings.OPENROUTER_URL, headers=headers, data=json.dumps(payload), timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        
        # простой backoff на перегрузку/сеть
        if resp.status_code in (429, 500, 502, 503, 504) and attempt < retries:
            time.sleep(1.5 * (attempt + 1))
            continue
        # если ретраем не помогло — кинем подробную ошибку
        try:
            msg = resp.json()

        except Exception:
            msg = resp.text

        raise RuntimeError(f"OpenRouter error {resp.status_code}: {msg}")