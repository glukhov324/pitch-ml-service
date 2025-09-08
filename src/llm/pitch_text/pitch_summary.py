from string import Template
import json
from typing import Any, Dict

from src.llm.base_prompts import SYS_PLAIN
from src.llm.openrouter import call_openrouter



SUMMARY_TEMPLATE = Template(
    """Сделай краткое резюме выступления (3–5 предложений), по-русски, без воды и повторов.
Учти контекст и учитывай, что это итог после доуточняющих вопросов.

Контекст:
$context_json

Верни ТОЛЬКО текст резюме.
"""
)

def build_summary(context: Dict[str, Any]) -> str:

    ctx_json = json.dumps(context, ensure_ascii=False)
    prompt = SUMMARY_TEMPLATE.substitute(context_json=ctx_json)
    messages = [
        {"role": "system", "content": SYS_PLAIN},
        {"role": "user", "content": prompt}
    ]
    
    return call_openrouter(messages, temperature=0.2, max_tokens=400).strip()