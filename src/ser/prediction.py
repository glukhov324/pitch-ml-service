from typing import List, Tuple
import numpy as np
import torch
import torch.nn.functional as F

from src.ser.models import feature_extractor, ser_model, config
from src.ser.utils import get_audio_interval
from src.schemas.speech import AsrSegment, SpeechAnalyseResult, EmotionPrediction
from src.config import settings, emotion_type_dict



@torch.no_grad()
def predict_emotion(speech_array: str, 
                    sampling_rate: int, 
                    start: int, 
                    end: int) -> EmotionPrediction:
    
    speech = get_audio_interval(
        speech_array=speech_array,
        start=start,
        end=end
    )

    inputs = feature_extractor(
        raw_speech=speech, 
        sampling_rate=sampling_rate, 
        return_tensors="pt", 
        padding=True
    )
    inputs = {key: inputs[key].to(settings.DEVICE) for key in inputs}
    logits = ser_model(**inputs).logits

    scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    outputs = [{
        "emotion": emotion_type_dict[config.id2label[i]], 
        "score": f"{round(score * 100, settings.FLOAT_ROUND_RATE):.1f}%"
        } for i, score in enumerate(scores)]

    sorted_outputs = sorted(
        outputs,
        key=lambda x: float(x["score"].rstrip("%")),
        reverse=True
    )

    return sorted_outputs[0]



def compute_speech_metrics(speech_array: np.ndarray,
                           sentences: List[AsrSegment]) -> SpeechAnalyseResult:

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

    words_per_minute = (
        round((total_words / total_duration_sec) * 60, settings.FLOAT_ROUND_RATE)
        if total_duration_sec > 0 else 0.0
    )

    avg_sentence_length = total_words / len(sentences)

    emotion_percentage = (emotional_speech_count / len(sentences)) * 10

    return SpeechAnalyseResult(
        temp_rate=words_per_minute,
        emotion_mark=emotion_percentage,
        avg_sentences_len=avg_sentence_length
    ).model_dump()