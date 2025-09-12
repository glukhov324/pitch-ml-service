from string import Template
from typing import Dict, Any
import re

from src.config import constants, settings
from src.llm.utils import extract_first_json
from src.llm.openrouter import call_openrouter


ALL_FILLERS = [
    "ээ", "эээ", "ээээ", "эээээ", "ээээээ",
    "аа", "ааа", "аааа", "ааааа", "аааааа",
    "эм", "эмм", "эммм", "эмммм", "эммммм",
    "мм", "ммм", "мммм", "ммммм", "мммммм",
    "хм", "хмм", "хммм", "хмммм", "хммммм",
    "э-э", "э-э-э", "э-э-э-э",
    "а-а", "а-а-а", "а-а-а-а",
    "о-о", "о-о-о",
    "у-у", "у-у-у",
    "ы-ы", "ы-ы-ы",
    "йй", "ййй", "йййй",
    "хх", "ххх", "хххх",
    "шш", "шшш", "шшшш",
    "фф", "ффф", "фффф",
    "сс", "ссс", "сссс",
    "ээ-эм", "эм-ээ", "аа-эм", "эм-аа",
    "хм-ээ", "ээ-хм", "мм-э", "э-мм",
    "э-ээ", "ээ-э", "а-аа", "аа-а",
    "э-эм", "эм-э", "а-эм", "эм-а",
    "хм-а", "а-хм", "мм-ээ", "ээ-мм",
    "эээ-мм", "мм-эээ", "хм-эээ", "эээ-хм",
    "ээ-мм-аа", "аа-ээ-хм", "эм-ээ-мм",
    "хм-ээ-аа-мм", "аа-мм-ээ-хм",
    "эээ...", "эммм...", "ааа...", "хмм...",
    "эээ?", "эмм?", "аа?", "хм?",
    "эээ!", "эмм!", "аа!", "хм!",
    "блин", "блинн", "блиннн", "блинннн",
    "ой", "ой-ой", "ой-ой-ой",
    "ух", "ухх", "уххх",
    "ай", "ай-ай", "ай-ай-ай",
    "ууу", "ааааааа", "эээээээ",
    "мммммм", "хммммм", "ээээээ",
    "пфф", "пф-пф", "пф-ф", "пф-ф-ф",
    "тсс", "тссс",
    "ббб", "бббб", "ббббб",
    "ззз", "зззз", "ззззз",
    "м-м-м", "мм-мм", "э-м-м", "эм-м", "э-ммм",
    "ах", "ах-ах", "ухх", "хах", "хахах",
    "х-х-х", "хх-хх", "х-х",
    "п-п-п", "п-п",
    "э-э-э-э-э", "а-а-а-а-а",
    "мм-мм-мм", "хм-хм-хм", "ы-ы-ы-ы", "й-й-й-й",
]


def convert_filler_dict_to_list(filler_counts: dict, sort_by_count: bool = False) -> list:
    result = [{"word": word, "count": count} for word, count in filler_counts.items()]
    if sort_by_count:
        result.sort(key=lambda x: x["count"], reverse=True)
    return result

def get_fillers(pitch_text: str):
    tl = pitch_text.lower()
    counts = {}
    for f in ALL_FILLERS:
        # точное слово/фраза
        hits = len(re.findall(rf"(?<!\w){re.escape(f)}(?!\w)", tl))
        if hits:
            counts[f] = hits
    temp_dict = dict(sorted(counts.items(), key=lambda x: -x[1]))
    return convert_filler_dict_to_list(temp_dict)