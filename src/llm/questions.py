from string import Template
import json
from typing import Any, Dict

from src.llm.base_prompts import SYS_JSON
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter



NEXT_QUESTION_TEMPLATE = Template(
    """Сформулируй ОДИН следующий короткий, практичный вопрос по выступлению.
Задача — уточнить пропавший важный контекст (цель, аудитория, метрики/цифры, сроки, призыв к действию).
Если всё уже понятно — верни {"ask": false, "question": ""}.

Входные данные (JSON):
$context_json

Формат ответа (строго JSON):
{
  "ask": true,
  "question": "один вопрос по-русски, максимально конкретный и короткий"
}
или
{
  "ask": false,
  "question": ""
}
Только JSON.
"""
)

def next_question(context: Dict[str, Any]) -> Dict[str, Any]:
    
    ctx_json = json.dumps(context, ensure_ascii=False)
    prompt = NEXT_QUESTION_TEMPLATE.substitute(context_json=ctx_json)
    messages = [
        {"role": "system", "content": SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    raw = call_openrouter(messages, temperature=0.1, max_tokens=200)
    obj = extract_first_json(raw)

    return {"ask": bool(obj.get("ask", False)), 
            "question": (obj.get("question") or "").strip()}