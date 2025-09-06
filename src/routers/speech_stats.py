from fastapi import APIRouter, UploadFile
import io
import torchaudio
from typing import List

from src.asr import get_asr_prediction
from src.ser import predict_emotion_full_audio
from src.schemas import  AsrEmotionSegment
from src.logger import logger




router = APIRouter(prefix="/analyze_speech")


@router.post("/by_audio_file", response_model=List[AsrEmotionSegment])
async def analyze_audio_file(audio_file: UploadFile):
    
    audio_data = await audio_file.read()
    audio_stream = io.BytesIO(audio_data)

    speech_array, _sampling_rate = torchaudio.load(audio_stream)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech_array_res = resampler(speech_array).squeeze().numpy()

    logger.info("Start ASR process")
    asr_prediction = get_asr_prediction(speech_array_res)
    logger.info("End ASR process")

    logger.info("Start emotion recognition process")
    response = predict_emotion_full_audio(
        speech_array=speech_array_res,
        sentences=asr_prediction
    )
    logger.info("End emotion recognition process")

    return response