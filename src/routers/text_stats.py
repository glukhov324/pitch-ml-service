from fastapi import APIRouter, UploadFile
import io

from src.logger import logger
from src.routers.utils import prepare_presentation
from src.llm.pitch_text import evaluate_pitch_text
from src.llm.presentation import presentation_analyze_pipeline
from src.llm import generate_questions_text_presenation
from src.schemas import PitchTextAnalyticsResult, QuestionGeneration




router = APIRouter(prefix="/text")


@router.post(
    path="/get_text_analytics", 
    response_model=PitchTextAnalyticsResult
)
async def analyze_text(
    text: str
):
    
    response = evaluate_pitch_text(
        base_text=text
    )

    return response


@router.post(
    path="/get_presentation_pitch_analytics"
)
async def analyze_presentation_pitch_text(text: str,
                                          presentation: UploadFile):
    
    slides_data = await prepare_presentation(presentation)

    response = presentation_analyze_pipeline(
        speech_text=text,
        pptx_bytes=slides_data
    )

    return response


@router.post("/get_questions_text_presentation", response_model=QuestionGeneration)
async def get_questions_text_presentation(
    text: str,
    n_questions: int,
    presentation: UploadFile | None = None
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