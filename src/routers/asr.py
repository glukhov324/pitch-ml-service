from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
from src.asr.prediction import get_asr_prediction, align_asr_prediction
import io
import librosa

from src.logger import logger
from src.schemas import AsrResult, Msg
from src.settings import settings



router = APIRouter(prefix="/automatic_speech_recognition")


@router.post("/by_file", response_model=AsrResult)
async def asr_by_file(audio_file: UploadFile):
    
    audio_data = await audio_file.read()

    audio_stream = io.BytesIO(audio_data)
    waveform , _ = librosa.load(audio_stream)

    raw_asr_prediction = get_asr_prediction(waveform)
    aligned_asr_prediction = align_asr_prediction(waveform, raw_asr_prediction)
    response = AsrResult(text=aligned_asr_prediction).model_dump()
    
    if not response:
        return JSONResponse(
            content=Msg(msg=f"Используется аудио с неподдерживаемым для сервиса языком. \
                        Список доступных языков: {settings.AVAILABLE_LANGUAGES}"),
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return response