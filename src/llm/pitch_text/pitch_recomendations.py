from string import Template
import json
from typing import Any, Dict, List

from src.llm.base_prompts import SYS_JSON
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter



RECOMMENDATIONS_TEMPLATE = Template(
    """Сформируй практичные рекомендации по улучшению выступления на русском.
Опирайся на оценки, обнаруженные проблемы и контекст. Будь конкретным, добавь пример переформулировки (до → после).

Входные данные:
$data_json

Формат ответа (строго JSON):
{
  "advices": [
    {
      "title": "короткий заголовок",
      "importance": "высокая|средняя|низкая",
      "reason": "почему это важно (1–2 фразы)",
      "todo": "императив, максимально конкретно",
      "example": "пример до → после по-русски, с цифрами если уместно"
    }
  ]
}
Только JSON.
"""
)

def build_recommendations(context: Dict[str, Any], 
                          evaluation: Dict[str, Any]) -> List[Dict[str, Any]]:
    
    data = {
        "контекст": context,
        "оценки": evaluation.get("marks", {}),
        "обнаруженные_проблемы": evaluation.get("issues", []),
        "отсутствующие_блоки": evaluation.get("missing_blocks", []),
    }
    data_json = json.dumps(data, ensure_ascii=False)
    prompt = RECOMMENDATIONS_TEMPLATE.substitute(data_json=data_json)
    messages = [
        {"role": "system", "content": SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    raw = call_openrouter(messages, temperature=0.2, max_tokens=900)
    obj = extract_first_json(raw)
    return obj.get("advices", [])[:10]