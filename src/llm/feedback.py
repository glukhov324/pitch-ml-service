import json

from src.config import constants, settings
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

Сгенерируй список плюсов (максимум 5), список минусов (максимум 5) для выступления (максимум 5), общая обратная связь (feedback). Текст выступления и презентация
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
  ],
  "feedback": ""
}}
"""
    messages = [
        {"role": "system", "content": constants.SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    logger.info("Start recommendation generation process")
    raw = call_openrouter(
        messages=messages, 
        temperature=settings.TEMPERATURE, 
        max_tokens=settings.MAX_TOKENS)
    logger.info("End recommendation generation process")

    logger.info(raw)

    return extract_first_json(raw)