import whisperx
import numpy as np

from src.asr.models import model_whisper, align_models_metadata
from src.settings import settings
from src.schemas import RawAsrPrediction



def get_asr_prediction(waveform: np.ndarray) -> RawAsrPrediction:
    
    transcription = model_whisper.transcribe(
        audio=waveform,
        batch_size=settings.BATCH_SIZE
    )

    return transcription


def align_asr_prediction(waveform: np.ndarray,
                         transcription: RawAsrPrediction) -> str:
    
    text = None
    if transcription["language"] in settings.AVAILABLE_LANGUAGES:

        align_model, metadata = align_models_metadata[transcription["language"]]
        align_result = whisperx.align(
            transcript=transcription["segments"], 
            model=align_model, 
            align_model_metadata=metadata, 
            audio=waveform, 
            device=settings.DEVICE, 
            return_char_alignments=False
        )
        
        text = ''.join([segment["text"] for segment in align_result["segments"]])

    return text