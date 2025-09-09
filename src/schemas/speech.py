from pydantic import BaseModel



class Timestamp(BaseModel):
    start: float
    end: float


class AsrSegment(Timestamp):
    text: str


class EmotionPrediction(BaseModel):
    emotion: str
    score: str

    
class AsrEmotionSegment(AsrSegment):
    emotion_data: EmotionPrediction

class SpeechAnalyseResult(BaseModel):
    pace_rate: float
    pace_mark: float
    emotion_mark: float
    avg_sentences_len: float