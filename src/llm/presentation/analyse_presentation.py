import json
from src.llm.openrouter import call_openrouter
from src.llm.utils import extract_first_json
from src.llm.base_prompts import SYS_JSON



def analyze_presentation(slides_data, metrics, speech_text):
    prompt = f"""
Ты — эксперт по презентациям.
Вот текст выступления:
\"\"\"{speech_text}\"\"\"

Вот извлечённые данные о слайдах:
{json.dumps(slides_data, ensure_ascii=False, indent=2)}

И метрики:
{json.dumps(metrics, ensure_ascii=False, indent=2)}

Сформируй JSON:
{{
  "соответствие": "высокое/среднее/низкое",
  "замечания": ["текст выступления не совпадает с слайдами", "..."],
  "баланс": "слишком много текста / оптимально / слишком много картинок",
  "рекомендации": [
    {{"заголовок":"...", "что_сделать":"...", "пример":"..."}}
  ]
}}
"""
    messages = [
        {"role": "system", "content": SYS_JSON},
        {"role": "user", "content": prompt}
    ]

    return call_openrouter(messages, temperature=0.1, max_tokens=400)


def analyze_presentation_json(slides_data, metrics, speech_text):
    raw = analyze_presentation(slides_data, metrics, speech_text)
    return extract_first_json(raw)