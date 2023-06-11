from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path

@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_learning_rate: float
    params_classes: int
    params_batch_size: int
    params_epochs: int

@dataclass(frozen=True)
class PrepareBaseTokenizerConfig:
    root_dir: Path
    base_tokenizer_path: Path