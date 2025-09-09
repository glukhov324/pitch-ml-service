import numpy as np
from typing import List

from src.speech_metrics.ser import predict_emotion
from src.speech_metrics.utils import pace_to_mark
from src.schemas.speech import AsrSegment, SpeechAnalyseResult
from src.config import settings



def compute_speech_metrics(
    speech_array: np.ndarray,
    sentences: List[AsrSegment]
) -> SpeechAnalyseResult:

    if not sentences:
        return SpeechAnalyseResult(
            temp_rate=0.0,
            emotion_mark=0.0,
            avg_sentences_len=0.0
        ).model_dump()

    total_words = 0
    total_duration_sec = 0.0
    emotional_speech_count = 0

    for sentence in sentences:
        start_ms = int(sentence["start"])
        end_ms = int(sentence["end"])

        emotion_result = predict_emotion(
            speech_array=speech_array,
            sampling_rate=settings.SER_SAMPLING_RATE,
            start=start_ms,
            end=end_ms
        )

        sentence["emotion_data"] = emotion_result

        if emotion_result["emotion"] == "эмоциональная речь":
            emotional_speech_count += 1

        total_duration_sec += sentence["end"] - sentence["start"]
        total_words += len(sentence["text"].split())

    pace_rate = (
        round((total_words / total_duration_sec) * 60, settings.FLOAT_ROUND_RATE)
        if total_duration_sec > 0 else 0.0
    )

    avg_sentence_length = total_words / len(sentences)

    emotion_percentage = (emotional_speech_count / len(sentences)) * 10

    return SpeechAnalyseResult(
        pace_rate=pace_rate,
        pace_mark=pace_to_mark(pace_rate),
        emotion_mark=emotion_percentage,
        avg_sentences_len=avg_sentence_length
    ).model_dump()