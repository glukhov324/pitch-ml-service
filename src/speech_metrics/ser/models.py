from transformers import AutoConfig, AutoModel, Wav2Vec2FeatureExtractor
import torch
from src.config import settings



config = AutoConfig.from_pretrained(
    pretrained_model_name_or_path=settings.SER_MODEL_NAME, 
    trust_remote_code=True
)
ser_model = AutoModel.from_pretrained(
    pretrained_model_name_or_path=settings.SER_MODEL_NAME, 
    trust_remote_code=True
)
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
    pretrained_model_name_or_path=settings.SER_MODEL_NAME
)

ser_model.to(settings.DEVICE)
