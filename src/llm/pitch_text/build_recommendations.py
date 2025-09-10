import json

from src.llm.base_prompts import SYS_JSON
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter
from src.logger import logger



def generate_feedback(
    pitch_text: str,
    slides_data = None
):
    
    processed_slides_data = {json.dumps(slides_data, ensure_ascii=False, indent=2)} if slides_data else None
    prompt = f"""
Ты — эксперт по презентациям и анализу текстов выступлений.
Вот текст выступления:
\"\"\"{pitch_text}\"\"\"

Вот извлечённые данные о слайдах (Может быть None, так как загрузка презентации опциональна):
{processed_slides_data}

Сгенерируй список плюсов (максимум 5), список минусов (максимум 5) для выступления (максимум 5). Текст выступления и презентация
Сформируй СТРОГО JSON! :
{{
  "pros": [
    "...",
    "...",
  ],
  "cons": [
    "...",
    "...",
  ],
  "recommendations": [
    "...",
    "...",
  ]
}}
"""
    messages = [
        {"role": "system", "content": SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    logger.info("Start recommendation generation process")
    raw = call_openrouter(messages, temperature=0.1, max_tokens=1200)
    logger.info("End recommendation generation process")

    logger.info(raw)

    return extract_first_json(raw)