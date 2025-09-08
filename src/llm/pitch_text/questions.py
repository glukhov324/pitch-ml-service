import json

from src.llm.base_prompts import SYS_JSON
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter



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
        {"role": "system", "content": SYS_JSON},
        {"role": "user", "content": prompt}
    ]

    raw = call_openrouter(messages, temperature=0.1, max_tokens=400)
    return extract_first_json(raw)