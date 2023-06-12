from EVE_AI.constants import *
import os
from EVE_AI.utils.common import read_yaml, create_directories
from EVE_AI.entity.config_entity import (DataIngestionConfig, PrepareBaseModelConfig, PrepareBaseTokenizerConfig, PrepareCallbacksConfig)

class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config_model = self.config.prepare_base_model

        create_directories([config_model.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config_model.root_dir),
            base_model_path=Path(config_model.base_model_path),
            params_learning_rate=self.params.LEARNING_RATE,
            params_iterations=self.params.ITERATIONS,
            params_depth=self.params.DEPTH
        )

        return prepare_base_model_config

    def get_prepare_base_tokenizer_config(self) -> PrepareBaseTokenizerConfig:
        config_tokenizer = self.config.prepare_base_tokenizer

        create_directories([config_tokenizer.root_dir])

        prepare_base_tokenizer_config = PrepareBaseTokenizerConfig(
            root_dir=Path(config_tokenizer.root_dir),
            base_tokenizer_path=Path(config_tokenizer.base_tokenizer_path)
        )

        return prepare_base_tokenizer_config

    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        config = self.config.prepare_callbacks
        model_ckpt_dir = os.path.dirname(config.checkpoint_model_filepath)
        create_directories([
            Path(model_ckpt_dir),
            Path(config.tensorboard_root_log_dir)
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.root_dir),
            tensorboard_root_log_dir=Path(config.tensorboard_root_log_dir),
            checkpoint_model_filepath=Path(config.checkpoint_model_filepath)
        )

        return prepare_callback_config
