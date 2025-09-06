import numpy as np
from src.config import settings



def get_audio_interval(speech_array: np.ndarray,
                       start: int,
                       end: int) -> np.ndarray:

    if len(speech_array.shape) > 1:
        speech_array = speech_array[0]

    start = start * settings.SER_SAMPLING_RATE
    end = end * settings.SER_SAMPLING_RATE
    speech_array = speech_array[start:end]

    return speech_array