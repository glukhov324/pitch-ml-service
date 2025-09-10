import json

from src.config import constants, settings
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter
from src.logger import logger



def generate_questions_text_presenation(speech_text: str,
                                        n_questions: int,
                                        slides_data = None):
    
    processed_slides_data = {json.dumps(slides_data, ensure_ascii=False, indent=2)} if slides_data else None
    prompt = f"""
Ты — эксперт по презентациям и анализу текстов выступлений.
Вот текст выступления:
\"\"\"{speech_text}\"\"\"

Вот извлечённые данные о слайдах (Может быть None, так как загрузка презентации опциональна):
{processed_slides_data}

Сгенерируй {n_questions} вопросов по имеющимся данным
Вопросы обязательно должны быть по тексту и презентации (если она загружена)
Сформируй JSON:
{{
  "questions": [
    "...",
    "...",
  ]
}}
"""
    messages = [
        {"role": "system", "content": constants.SYS_JSON},
        {"role": "user", "content": prompt}
    ]
    logger.info("Start questions generation process")
    raw = call_openrouter(
        messages=messages, 
        temperature=settings.TEMPERATURE, 
        max_tokens=settings.MAX_TOKENS)
    logger.info("End questions generation process")

    return extract_first_json(raw)