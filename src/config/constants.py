from typing import List, Tuple, Dict, Callable



class Constants:

    emotion_type_dict: Dict[str, str]  = {
            'anger': 'эмоциональная речь',
            'disgust': 'эмоциональная речь',
            'enthusiasm': 'эмоциональная речь',
            'happiness': 'эмоциональная речь',
            'fear': 'робкая речь',
            'neutral': 'монотонная речь',
            'sadness': 'монотонная речь'
        }
    pace_zones: List[Tuple[float, float, Callable[[float], float]]] = [
            (90, 110, lambda p: (p - 90) / 20 * 7),           
            (110, 150, lambda p: 10 - abs(p - 130) / 20 * 3),
            (150, 180, lambda p: (180 - p) / 30 * 7),        
        ]
    SYS_JSON: str = "Отвечай строго валидным JSON по схеме. Без пояснений и без Markdown."
    

constants = Constants()