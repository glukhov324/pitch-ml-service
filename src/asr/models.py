from faster_whisper import WhisperModel
from src.config import settings



# Run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8

whisper_model = WhisperModel(
    model_size_or_path=settings.WHISPER_MODEL_SIZE, 
    device=settings.DEVICE, 
    compute_type=settings.WHISPER_COMPUTE_TYPE,
    cpu_threads=settings.NUM_THREADS,
    num_workers=settings.NUM_WORKERS
)