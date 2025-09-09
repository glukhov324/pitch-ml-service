import numpy as np
from src.config import settings, constants



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
    Оценка строится по принципу "чем ближе к идеальному диапазону — тем выше балл":
    - Медленно (90–110): линейно от 0 до 7
    - Идеально (110–150): пик 10 в центре (130), спадает до 7 на границах
    - Быстро (150–180): линейно от 7 до 0

    Args:
        pace (float): темп в ударах в минуту (число)

    :return: оценка темпа речи по 10-балльной шкале (float от 1.0 до 10.0)
    """

    # Проверяем каждую зону
    for min_p, max_p, score_fn in constants.pace_zones:
        if min_p <= pace <= max_p:
            return score_fn(pace)

    return 0.0