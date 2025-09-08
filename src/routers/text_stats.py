from fastapi import APIRouter, UploadFile
import io


from src.logger import logger
from src.llm.pitch_text import pitch_text_analyze_pipeline
from src.llm.presentation.pypeline import presentation_analyze_pypeline
from src.schemas import PitchEvaluationResult




router = APIRouter(prefix="/text")


@router.post("/get_pitch_text_analytics", response_model=PitchEvaluationResult)
async def analyze_pitch_text(text: str):
    
    response = pitch_text_analyze_pipeline(
        base_text=text
    )

    return response


@router.post("/get_presentation_analytics")
async def analyze_pitch_text(text: str,
                             presentation: UploadFile):
    
    pptx_data = await presentation.read()
    audio_stream = io.BytesIO(pptx_data)

    response = presentation_analyze_pypeline(
        speech_text=text,
        pptx_bytes=audio_stream
    )

    return response