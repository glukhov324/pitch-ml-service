from fastapi import (
    APIRouter, 
    UploadFile, 
    File, 
    Depends
)
from typing import List

from src.asr import get_asr_prediction
from src.ser import compute_speech_metrics
from src.schemas import AsrSegment, SpeechAnalyseResult
from src.routers.utils import prepare_audio, parse_segments_json
from src.logger import logger



router = APIRouter(prefix="/speech")



@router.post("/transcribe_speech", response_model=List[AsrSegment])
async def get_speech_transcription(audio_file: UploadFile):
    
    speech_array = await prepare_audio(audio_file)

    logger.info("Start ASR process")
    transcription = get_asr_prediction(speech_array)
    logger.info("End ASR process")

    return transcription


@router.post("/get_speech_metrics", response_model=SpeechAnalyseResult)
async def get_speech_metrics(audio_file: UploadFile = File(...),
                             text_timestamps: List[AsrSegment] = Depends(parse_segments_json)):
    
    speech_array_res = await prepare_audio(audio_file)

    logger.info("Start statistic generation process")
    response = compute_speech_metrics(
        speech_array=speech_array_res,
        sentences=text_timestamps
    )
    logger.info("End statistic generation process")

    return response