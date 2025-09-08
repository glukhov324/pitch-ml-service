from pydantic import BaseModel
from typing import List



class Context(BaseModel):
    pitch_text: str


class PitchMarks(BaseModel):
    structure: int
    clarity: int
    specificity: int
    persuasiveness: int


class CompletePitchMarksBlock(BaseModel):
    marks: PitchMarks
    missing_blocks: List[str]
    issues: List[str]


class Advice(BaseModel):
    title: str
    importance: str
    reason: str
    todo: str
    example: str


class PitchEvaluationResult(BaseModel):
    context: Context
    pitch_evaluation: CompletePitchMarksBlock
    advices: List[Advice]
    pitch_summary: str