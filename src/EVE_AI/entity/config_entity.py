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
    params_learning_rate: float
    params_depth: int
    params_iterations: int

@dataclass(frozen=True)
class PrepareBaseTokenizerConfig:
    root_dir: Path
    base_tokenizer_path: Path

@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    base_model_path: Path
    base_tokenizer_path: Path
    fitted_tokenizer_path: Path
    training_data: Path
    validation_data: Path
    params_verbose: int

@dataclass(frozen=True)
class EvaluationConfig:
    path_of_model: Path
    path_of_tokenizer: Path
    test_data: Path
    all_params: dict