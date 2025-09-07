import numpy as np

from src.asr.models import whisper_model
from src.asr.utils import segments_to_sentences
from src.config import settings



def get_asr_prediction(speech_array: np.ndarray):
    
    segments, _ = whisper_model.transcribe(
        audio=speech_array, 
        beam_size=settings.WHISPER_BEAM_SIZE,
    )

    res_segments = [{"start": round(elem.start, settings.FLOAT_ROUND_RATE),
                     "end": round(elem.end, settings.FLOAT_ROUND_RATE),
                     "text": elem.text} for elem in segments]
    
    asr_result = segments_to_sentences(res_segments)

    return asr_result