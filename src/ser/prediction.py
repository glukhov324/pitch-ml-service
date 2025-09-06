from typing import List
import numpy as np
import torch
import torch.nn.functional as F

from src.ser.models import feature_extractor, ser_model, config
from src.ser.utils import get_audio_interval
from src.schemas.speech import AsrSegment
from src.config import settings, emotion_type_dict



@torch.no_grad()
def predict_emotion(speech_array: str, 
                    sampling_rate: int, 
                    start: int, 
                    end: int):
    
    speech = get_audio_interval(
        speech_array=speech_array,
        start=start,
        end=end
    )

    inputs = feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
    inputs = {key: inputs[key].to(settings.DEVICE) for key in inputs}
    logits = ser_model(**inputs).logits

    scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    outputs = [{"emotion": emotion_type_dict[config.id2label[i]], "score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]

    sorted_outputs = sorted(
        outputs,
        key=lambda x: float(x["score"].rstrip("%")),
        reverse=True
    )
    return sorted_outputs[0]



def predict_emotion_full_audio(speech_array: np.ndarray,
                               sentences: List[AsrSegment]):
    
    for i in range(len(sentences)):
        elem = sentences[i]
        print(f"Начало: {elem['start']}, конец: {elem['end']}")

        start = int(elem['start'])
        end = int(elem['end'])

        res = predict_emotion(
            speech_array=speech_array,
            sampling_rate=settings.SER_SAMPLING_RATE,
            start=start,
            end=end
        )
        sentences[i]["emotion_data"] = res
    
    return sentences