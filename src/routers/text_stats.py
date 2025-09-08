from fastapi import APIRouter, UploadFile
import io

from src.logger import logger
from src.llm.utils import get_slides_data
from src.llm.pitch_text import pitch_text_analyze_pipeline
from src.llm.presentation.pipeline import presentation_analyze_pipeline
from src.llm import generate_questions_text_presenation
from src.schemas import PitchEvaluationResult, QuestionGeneration




router = APIRouter(prefix="/text")


@router.post("/get_pitch_text_analytics", response_model=PitchEvaluationResult)
async def analyze_pitch_text(text: str):
    
    response = pitch_text_analyze_pipeline(
        base_text=text
    )

    return response


# @router.post("/get_presentation_analytics")
# async def analyze_pitch_text(text: str,
#                              presentation: UploadFile):
    
#     pptx_data = await presentation.read()
#     pptx_bytes = io.BytesIO(pptx_data)

#     response = presentation_analyze_pipeline(
#         speech_text=text,
#         pptx_bytes=pptx_bytes
#     )

#     return response


@router.post("/get_questions_text_presentation", response_model=QuestionGeneration)
async def get_questions_text_presentation(text: str,
                                          n_questions: int,
                                          presentation: UploadFile | None = None):
    
    slides_data = None
    if presentation:
        pptx_data = await presentation.read()
        pptx_bytes = io.BytesIO(pptx_data)
        slides_data = get_slides_data(pptx_bytes)
    
    logger.info("Start questions generation process")
    response = generate_questions_text_presenation(
        speech_text=text,
        n_questions=n_questions,
        slides_data=slides_data
    )
    logger.info("End questions generation process")

    return response