from pydantic import BaseModel
from typing import List



class Context(BaseModel):
    pitch_text: str


class PitchMarks(BaseModel):
    structure: int
    clarity: int
    specificity: int
    persuasiveness: int


class FillerWord(BaseModel):
    word: str
    count: int


class PitchTextAnalyticsResult(BaseModel):
    marks: PitchMarks
    filler_words: List[FillerWord] | None = None
    hesitant_phrases: List[str] | None = None
    unclarity_moments: List[str] | None = None


class TextPresentationFeedback(BaseModel):
    pros: List[str]
    cons: List[str]
    recommendations: List[str]


class Advice(BaseModel):
    title: str
    importance: str
    reason: str
    todo: str
    example: str


class QuestionGeneration(BaseModel):
    questions: List[str]