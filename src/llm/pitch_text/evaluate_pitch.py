from string import Template
from typing import Dict, Any
import json

from src.llm.base_prompts import SYS_JSON
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter



EVALUATE_TEMPLATE = Template(
    """Оцени качество выступления по рубрике 0..10.
Метрики (русские названия):
- "структура (structure)": есть ли последовательность вступление → проблема → решение → доказательства (цифры/кейсы) → ценность → призыв к действию
- "ясность (clarity)": простота языка, отсутствие сложных конструкций, читаемость
- "конкретика (specificity)": наличие фактов, цифр, сроков, сравнений
- "убедительность (persuasiveness)": выгода для аудитории, сила аргументов, чёткий следующий шаг

Также верни:
- "отсутствующие_блоки (missing_blocks)": какие структурные блоки отсутствуют (из: "вступление","проблема","решение","доказательства","ценность","призыв")
- "обнаруженные_проблемы (issues)": значения из: "паразиты","жаргон","канцелярит","пассив","нет_цифр","длинные_предложения","слабый_CTA","фокус_на_мы"

Контекст:
$context_json

Формат ответа (строго JSON):
{
  "marks": {"structure":0,"clarity":0,"specificity":0,"persuasiveness":0},
  "missing_blocks": [],
  "issues": []
}
Только JSON.
"""
)

def evaluate_presentation(context: Dict[str, Any]) -> Dict[str, Any]:

    ctx_json = json.dumps(context, ensure_ascii=False)
    prompt = EVALUATE_TEMPLATE.substitute(context_json=ctx_json)
    messages = [
        {"role": "system", "content": SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    raw = call_openrouter(messages, temperature=0.1, max_tokens=400)
    
    return extract_first_json(raw)