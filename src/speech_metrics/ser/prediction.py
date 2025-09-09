from typing import List
import numpy as np
import torch
import torch.nn.functional as F

from src.speech_metrics.ser.models import feature_extractor, ser_model, config
from src.speech_metrics.utils import get_audio_interval
from src.schemas.speech import EmotionPrediction
from src.config import settings, emotion_type_dict



@torch.no_grad()
def predict_emotion(
    speech_array: str, 
    sampling_rate: int, 
    start: int, 
    end: int
) -> EmotionPrediction:
    
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