from typing import List
from src.schemas.speech import AsrSegment



def segments_to_sentences(predicted_segments: List[AsrSegment]) -> List[AsrSegment]:

    sentences = []
    current_sentence = ""
    current_start = None  

    for i, seg in enumerate(predicted_segments):
        text = seg['text'].strip()

        if current_start is None:
            current_start = seg['start']

        current_sentence += " " + text
        current_sentence = current_sentence.strip()

        if text.endswith('.'):
            sentences.append({
                'start': current_start,
                'end': seg['end'],
                'text': current_sentence
            })
            
            current_sentence = ""
            current_start = None
    
    return sentences