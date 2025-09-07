from fastapi import APIRouter, UploadFile
import io
import torchaudio
from typing import List

from src.asr import get_asr_prediction
from src.ser import get_all_emotions_with_speech_rate
from src.schemas import  AsrEmotionSegment, SpeechAnalyseResult
from src.logger import logger




router = APIRouter(prefix="/analyze_speech")


@router.post("/by_audio_file", response_model=SpeechAnalyseResult)
async def analyze_audio_file(audio_file: UploadFile):
    
    audio_data = await audio_file.read()
    audio_stream = io.BytesIO(audio_data)

    speech_array, _sampling_rate = torchaudio.load(audio_stream)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech_array_res = resampler(speech_array).squeeze().numpy()

    if len(speech_array_res.shape) > 1:
        speech_array_res = speech_array_res[0]

    logger.info("Start ASR process")
    asr_prediction = get_asr_prediction(speech_array_res)
    logger.info("End ASR process")

    logger.info("Start emotion recognition process")
    emotions_asr, wpe = get_all_emotions_with_speech_rate(
        speech_array=speech_array_res,
        sentences=asr_prediction
    )
    logger.info("End emotion recognition process")

    response = SpeechAnalyseResult(
        speech_segments=emotions_asr,
        temp_rate=wpe
    ).model_dump()

    return response