from EVE_AI.constants import *
import os
from EVE_AI.utils.common import read_yaml, create_directories
from EVE_AI.entity.config_entity import (DataIngestionConfig, PrepareBaseModelConfig,
                                         PrepareBaseTokenizerConfig, TrainingConfig,
                                         EvaluationConfig, BaseConfig)


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

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        prepare_base_tokenizer = self.config.prepare_base_tokenizer
        prepare_fitted_tokenizer = self.config.prepare_fitted_tokenizer
        preprocessor = self.config.preprocessor
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "training.csv")
        validation_data = os.path.join(self.config.data_ingestion.unzip_dir, "validation.csv")
        create_directories([
            Path(training.root_dir),
            Path(prepare_fitted_tokenizer.root_dir),
            Path(preprocessor.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            base_model_path=Path(prepare_base_model.base_model_path),
            base_tokenizer_path=Path(prepare_base_tokenizer.base_tokenizer_path),
            fitted_tokenizer_path=Path(prepare_fitted_tokenizer.fitted_tokenizer_path),
            preprocessor_path=Path(preprocessor.preprocessor_path),
            training_data=Path(training_data),
            validation_data=Path(validation_data),
            params_verbose=params.VERBOSE
        )

        return training_config

    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=Path(self.config.training.trained_model_path),
            path_of_tokenizer=Path(self.config.prepare_fitted_tokenizer.fitted_tokenizer_path),
            path_of_preprocessor=Path(self.config.preprocessor.preprocessor_path),
            test_data=Path(os.path.join(self.config.data_ingestion.unzip_dir, "test.csv")),
            all_params=self.params
        )
        return eval_config

    def get_base_config(self) -> BaseConfig:
        base = self.config.base
        create_directories([
            Path(base.root_dir)
        ])
        base_config = BaseConfig(
            root_dir=Path(base.root_dir),
            intent_data=Path(base.intent_data),
            base_preprocessor_path=Path(self.config.preprocessor.preprocessor_path),
            base_tokenizer_path=Path(self.config.prepare_base_tokenizer.base_tokenizer_path),
            fitted_tokenizer_path=Path(self.config.prepare_fitted_tokenizer.fitted_tokenizer_path),
            trained_model_path=Path(self.config.training.trained_model_path),
            distance_vectorizer_path=Path(base.distance_vectorizer_path),
            distance_vector_dict_path=Path(base.distance_vector_dict_path)
        )
        return base_config
