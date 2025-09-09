import numpy as np
from src.config import settings



def get_audio_interval(
    speech_array: np.ndarray,
    start: int,
    end: int
) -> np.ndarray:

    start = start * settings.SER_SAMPLING_RATE
    end = end * settings.SER_SAMPLING_RATE
    speech_array = speech_array[start:end]

    return speech_array


def pace_to_mark(
    pace: float
) -> float:
    """
    Переводит темп речи в 10-балльную шкалу.

    Args:
        pace (float): темп в ударах в минуту (число)

    :return: оценка темпа речи по 10-балльной шкале (float от 1.0 до 10.0)
    """

    min_pace = 90
    max_pace = 180

    pace = max(min_pace, min(max_pace, pace))

    score = 1.0 + (pace - min_pace) * (10.0 - 1.0) / (max_pace - min_pace)
    score = round(score, settings.FLOAT_ROUND_RATE)

    return score