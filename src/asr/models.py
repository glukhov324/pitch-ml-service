import whisperx
from src.settings import settings



model_whisper = whisperx.load_model(
    whisper_arch=settings.WHISPER_ARCH,
    device=settings.DEVICE,
    compute_type=settings.COMPUTE_TYPE
)

align_model_en, metadata_en = whisperx.load_align_model(language_code="en", device=settings.DEVICE)
align_model_ru, metadata_ru = whisperx.load_align_model(language_code="ru", device=settings.DEVICE)

align_models_metadata = {
    "ru": (align_model_ru, metadata_ru),
    "en": (align_model_en, metadata_en)
}