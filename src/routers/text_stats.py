from fastapi import APIRouter, UploadFile, File

from src.logger import logger
from src.routers.utils import prepare_presentation
from src.llm import (
    evaluate_pitch_text,
    generate_feedback,
    generate_questions_text_presenation,
    get_fillers
)
from src.schemas import (
    PitchTextAnalyticsResult,
    QuestionGeneration,
    TextPresentationFeedback
)


router = APIRouter(prefix="/text")


@router.post(
    path="/get_text_analytics", 
    response_model=PitchTextAnalyticsResult
)
async def analyze_text(
    text: str
):
    
    evaluation = evaluate_pitch_text(
        pitch_text=text
    )
    fillers = get_fillers(
        pitch_text=text
    )
    logger.info(fillers)

    evaluation["filler_words"] = fillers

    return evaluation


@router.post(
    path="/get_text_presentation_feedback",
    response_model=TextPresentationFeedback
)
async def get_text_presentation_feedback(
    text: str,
    presentation: UploadFile | str | None = None
):

    slides_data = None
    if presentation:
        slides_data = await prepare_presentation(presentation)

    response = generate_feedback(
        pitch_text=text,
        slides_data=slides_data
    )

    logger.info(response)

    return response


@router.post(
    path="/get_questions_text_presentation", 
    response_model=QuestionGeneration
)
async def get_questions_text_presentation(
    text: str,
    n_questions: int,
    presentation: UploadFile | str | None = None
):
    
    slides_data = None
    if presentation:
        slides_data = await prepare_presentation(presentation)
    
    response = generate_questions_text_presenation(
        speech_text=text,
        n_questions=n_questions,
        slides_data=slides_data
    )

    return response