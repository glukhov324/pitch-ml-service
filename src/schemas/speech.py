from pydantic import BaseModel
from typing import List



class TimestampBase(BaseModel):
    start: float
    end: float


class AsrSegment(TimestampBase):
    text: str


class EmotionBase(BaseModel):
    emotion: str
    score: str

    
class AsrEmotionSegment(AsrSegment):
    emotion_data: EmotionBase

class SpeechAnalyseResult(BaseModel):
    speech_segments: List[AsrEmotionSegment]
    temp_rate: float