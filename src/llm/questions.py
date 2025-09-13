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
Ты — строгий эксперт по презентациям и публичным выступлениям.
У тебя есть цель — помочь спикеру увидеть слабые места и незакрытые вопросы в его речи.

Вот текст выступления (это именно РАСШИФРОВКА УСТНОЙ РЕЧИ, а не написанный текст, поэтому не нужно оценивать орфографию или стиль письма):
{speech_text}

Вот извлечённые данные о слайдах (может быть None, если слайды не загружены):
{processed_slides_data}

Сгенерируй {n_questions} каверзных вопросов. 
Очень важно: 
- вопросы не должны быть пересказом фактов из презентации, а должны «тыкать» в слабые места, неясности и пробелы;  
- допускается лёгкая пассивная агрессия в формулировках;  
- вопросы должны подталкивать к защите идей, а не просто к воспроизведению информации;  
- если есть слайды — учитывай и текст, и слайды.

Формат ответа:
{
  "questions": [
    "...",
    "...",
  ]
}
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