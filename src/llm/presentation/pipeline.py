import io

from src.llm.utils import get_slides_data
from src.llm.presentation.compute_presentation_metrics import compute_ppt_metrics
from src.llm.presentation.analyse_presentation import analyze_presentation_json
from src.logger import logger




def presentation_analyze_pipeline(speech_text: str,
                                  pptx_bytes: io.BytesIO):
    """
    Анализируем PPTX (извлечение → базовые метрики → DeepSeek-оценка соответствия/баланса)
    """

    slides_data = get_slides_data(pptx_bytes)
    logger.info("Presntation loaded")

    logger.info("Start computing presntation metrics procces")
    ppt_metrics = compute_ppt_metrics(slides_data)
    logger.info("End computing presntation metrics procces")

    logger.info("Start generating LLM report procces")
    ppt_llm = analyze_presentation_json(slides_data, ppt_metrics, speech_text)
    logger.info("End generating LLM report procces")

    unified = {         
        "presentation_metrics": ppt_metrics,
        "llm_report": ppt_llm             
    }
    return unified