from string import Template
from typing import Dict, Any
import json
import re

from src.config import constants, settings
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter





EVALUATE_TEMPLATE = Template(
    """Оцени качество выступления по рубрике 0..10.
    Ты должен оценить текст высутпления, неуверенные фразы, непонятные моменты Анализируй выступление, даже если оно очень короткое
Метрики (русские названия):
- "структура (structure)": есть ли последовательность вступление → проблема → решение → доказательства (цифры/кейсы) → ценность → призыв к действию
- "ясность (clarity)": простота языка, отсутствие сложных конструкций, читаемость
- "конкретика (specificity)": наличие фактов, цифр, сроков, сравнений
- "убедительность (persuasiveness)": выгода для аудитории, сила аргументов, чёткий следующий шаг
- "уверенность формулировок (confidence)": уровень уверенности формулировок

Также верни:
- "фразы из скписка: кажется, наверное, возможно  (hesitant_phrases)": список подобных фраз из текста выстпуления, слова по типу ЭМ не подходят, не вставляй их в ответ ни в коем случае
- "непонятные моменты из текста выступления, суть которых ты не понял (unclarity_moments)": список непонятных моментов выступления

Контекст:
$context_json

Формат ответа (строго JSON):
{
  "marks": {"structure":0,"clarity":0,"specificity":0,"persuasiveness":0},
  "hesitant_phrases": ['кажется', 'наверное' и строго только такие слова],
  "unclarity_moments": ['непонятно, как работает модель' и тд]
}
Только JSON.
"""

)





def evaluate_pitch_text(pitch_text: str) -> Dict[str, Any]:

    context = {
        "pitch_text": pitch_text.strip()
    }
    ctx_json = json.dumps(context, ensure_ascii=False)
    prompt = EVALUATE_TEMPLATE.substitute(
        context_json=ctx_json
    )
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