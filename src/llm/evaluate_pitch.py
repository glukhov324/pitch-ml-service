from string import Template
from typing import Dict, Any
import json

from src.config import constants, settings
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter



EVALUATE_TEMPLATE = Template(
    """Оцени качество выступления по рубрике 0..10.
Метрики (русские названия):
- "структура (structure)": есть ли последовательность вступление → проблема → решение → доказательства (цифры/кейсы) → ценность → призыв к действию
- "ясность (clarity)": простота языка, отсутствие сложных конструкций, читаемость
- "конкретика (specificity)": наличие фактов, цифр, сроков, сравнений
- "убедительность (persuasiveness)": выгода для аудитории, сила аргументов, чёткий следующий шаг
- "уверенность формулировок (confidence)": уровень уверенности формулировок

Также верни:
- "топ-3 слов филлеров, например, эээ, ааа и тд (fillers_words)": список словарей, структура которых состоит из слова и его повторений. Пример: {'word': 'ээ', 'count': 15}
- "неуверенные фразы по формулировкам (hesitant_phrases)": список неуверенных фраз из текста выстпуления
- "непонятные моменты из текста выступления, суть которых ты не понял (unclarity_moments)": список непонятных моментов выступления

Контекст:
$context_json

Формат ответа (строго JSON):
{
  "marks": {"structure":0,"clarity":0,"specificity":0,"persuasiveness":0},
  "fillers_words": [{'word': 'ээ', 'count': 15}, {'word': 'эм', 'count': 10}, {'word': 'ааа', 'count': 7}]
  "hesitant_phrases": [],
  "unclarity_moments": []
}
Только JSON.
"""

)

def evaluate_pitch_text(pitch_text: str) -> Dict[str, Any]:

    context = {
        "pitch_text": pitch_text.strip()
    }
    ctx_json = json.dumps(context, ensure_ascii=False)
    prompt = EVALUATE_TEMPLATE.substitute(context_json=ctx_json)
    messages = [
        {"role": "system", "content": constants.SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    raw = call_openrouter(
        messages=messages, 
        temperature=settings.TEMPERATURE, 
        max_tokens=settings.MAX_TOKENS
    )
    
    return extract_first_json(raw)