from pydantic import BaseModel



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