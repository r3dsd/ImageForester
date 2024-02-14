from huggingface_hub import hf_hub_download
import os

from ..config import HF_CONFIG
from ..logger import get_logger

logger = get_logger(__name__)

class HFDownloader:
    def __init__(self, repo_id=HF_CONFIG['HF_REPO_ID'], base_dir=HF_CONFIG['HF_MODEL_DIR']):
        self.repo_id = repo_id
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)

    def download_model(self, model_file_name):
        logger.info(f"Checking for model {model_file_name} in cache or downloading from Hugging Face Hub...")
        model_path = hf_hub_download(repo_id=self.repo_id, filename=model_file_name, cache_dir=self.base_dir)
        return model_path