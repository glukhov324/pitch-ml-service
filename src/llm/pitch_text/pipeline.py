from typing import Dict, Any

from src.llm.questions import next_question
from src.llm.pitch_text.evaluate_pitch import evaluate_presentation
from src.llm.pitch_text.pitch_recomendations import build_recommendations
from src.llm.pitch_text.pitch_summary import build_summary
from src.logger import logger



def pitch_text_analyze_pipeline(base_text: str,
                                rounds: int = 3,
                                ask_gate: bool = True) -> Dict[str, Any]:
    """
    Обязательный порядок:
    текст -> LLM -> вопрос -> ответ (до 2–3 итераций, с пропуском) -> оценка -> советы -> резюме
    """
    
    context = {
        "pitch_text": base_text.strip()
    }

    # # Заглушка: хотим ли отвечать на вопросы?
    # if ask_gate:
    #     gate = input("Хотите ответить на уточняющие вопросы? (да/нет): ").strip().lower()
    #     if gate not in ("да", "yes", "y"):
    #         print("Пропускаем вопросы.")
    #         rounds = 0

    # # Диалог вопросов/ответов
    # for i in range(rounds):
    #     q = next_question(context)
    #     if not q.get("ask") or not q.get("question"):
    #         print("Вопросов больше нет.")
    #         break
    #     print(f"\nВопрос {i+1}: {q['question']}")
    #     ans = input("Ваш ответ (или оставьте пустым, чтобы пропустить): ").strip()
    #     if ans:
    #         # кладем ответ в доп. контекст
    #         context["доп_контекст"][f"ответ_{i+1}"] = {"вопрос": q["question"], "ответ": ans}
    #     else:
    #         print("Ответ пропущен.")

    # Оценка
    logger.info("Start evaluate presentation pitch text process")
    evaluation = evaluate_presentation(context)
    logger.info("End evaluate presentation pitch text process")

    # Советы
    logger.info("Start building recommendations process")
    advice = build_recommendations(context, evaluation)
    logger.info("End building recommendations process")

    # Резюме
    logger.info("Start building pitch summary process")
    summary = build_summary(context)
    logger.info("Start building pitch summary process")

    # Возврат итогов
    return {
        "pitch_evaluation": evaluation,
        "advices": advice,
        "pitch_summary": summary
    }