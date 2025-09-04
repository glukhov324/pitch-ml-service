from typing import List
from pydantic import BaseModel



class TimestampBase(BaseModel):
    start: float
    end: float

class RawAsrSegment(TimestampBase):
    text: str

class RawAsrPrediction(RawAsrSegment):
    segments: List[RawAsrSegment]
    language: str

class AsrResult(BaseModel):
    text: str