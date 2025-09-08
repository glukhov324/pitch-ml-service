from fastapi import UploadFile, Form, HTTPException
import io
import torchaudio
import numpy as np
from typing import List
import json

from src.schemas import AsrSegment



async def prepare_audio(audio_file: UploadFile) -> np.ndarray:
    
    audio_data = await audio_file.read()
    audio_stream = io.BytesIO(audio_data)

    speech_array, _sampling_rate = torchaudio.load(audio_stream)
    resampler = torchaudio.transforms.Resample(_sampling_rate)
    speech_array_res = resampler(speech_array).squeeze().numpy()

    if len(speech_array_res.shape) > 1:
        speech_array_res = speech_array_res[0]
    
    return speech_array_res


def parse_segments_json(
    text_timestamps: str = Form(
        ...,
        description="JSON-массив сегментов распознанной речи",
        example='[{"start": 0, "end": 5.0, "text": "Пример текста"}]'
    )
) -> List[AsrSegment]:
    try:
        data = json.loads(text_timestamps)
        return [AsrSegment(**item).model_dump() for item in data]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid segments JSON: {str(e)}")