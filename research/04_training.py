from dataclasses import dataclass
from EVE_AI.constants import *
from EVE_AI.utils.common import read_yaml, create_directories
import time
import os
import pickle
import pandas as pd
import tensorflow as tf


@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    base_model_path: Path
    base_tokenizer_path: Path
    fitted_tokenizer_path: Path
    training_data: Path
    validation_data: Path
    params_learning_rate: float
    params_depth: int
    params_verbose: int


@dataclass(frozen=True)
class PrepareCallbacksConfig:
    root_dir: Path
    tensorboard_root_log_dir: Path
    checkpoint_model_filepath: Path


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

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

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        prepare_base_tokenizer = self.config.prepare_base_tokenizer
        prepare_fitted_tokenizer = self.config.prepare_fitted_tokenizer
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "training.csv")
        validation_data = os.path.join(self.config.data_ingestion.unzip_dir, "validation.csv")
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            base_model_path=Path(prepare_base_model.base_model_path),
            base_tokenizer_path=Path(prepare_base_tokenizer.base_tokenizer_path),
            fitted_tokenizer_path=Path(prepare_fitted_tokenizer.fitted_tokenizer_path),
            training_data=Path(training_data),
            validation_data=Path(validation_data),
            params_learning_rate=params.LEARNING_RATE,
            params_depth=params.DEPTH,
            params_verbose=params.VERBOSE
        )

        return training_config


class PrepareCallback:
    def __init__(self, config: PrepareCallbacksConfig):
        self.config = config

    @property
    def _create_tb_callbacks(self):
        timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
        tb_running_log_dir = os.path.join(
            self.config.tensorboard_root_log_dir,
            f"tb_logs_at_{timestamp}",
        )
        return tf.keras.callbacks.TensorBoard(log_dir=tb_running_log_dir)

    @property
    def _create_ckpt_callbacks(self):
        return tf.keras.callbacks.ModelCheckpoint(
            filepath=self.config.checkpoint_model_filepath,
            save_best_only=True
        )

    def get_tb_ckpt_callbacks(self):
        return [
            self._create_tb_callbacks,
            self._create_ckpt_callbacks
        ]


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_base_model(self):
        with open(self.config.base_model_path, 'rb') as f:
            self.model = pickle.load(f)

    def get_tokenizer(self):
        with open(self.config.base_tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)

    def train_valid_generator(self):
        training_data_frame = pd.read_csv(self.config.training_data)
        self.train_text_generator = training_data_frame.iloc[:,0]
        self.train_labels_generator = training_data_frame.iloc[:,1]

        validation_data_frame = pd.read_csv(self.config.validation_data)
        self.valid_text_generator = validation_data_frame.iloc[:,0]
        self.valid_labels_generator = validation_data_frame.iloc[:,1]

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        with open(path, 'wb') as f:
            pickle.dump(model, f)

    def train(self):

        self.tokenized_training_data = self.tokenizer.fit_transform(self.train_text_generator.tolist())
        self.train_features = self.tokenized_training_data.toarray()

        self.save_model(path=self.config.fitted_tokenizer_path, model=self.train_features)

        self.tokenized_validation_data = self.tokenizer.transform(self.valid_text_generator.tolist())
        self.valid_features = self.tokenized_validation_data.toarray()

        self.train_labels = self.train_labels_generator
        self.valid_labels = self.valid_labels_generator

        self.model.fit(self.train_features,
                       self.train_labels,
                       eval_set=(self.valid_features, self.valid_labels),
                       verbose=self.config.params_verbose)

        self.save_model(path=self.config.trained_model_path, model=self.model)


try:
    config = ConfigurationManager()
    prepare_callbacks_config = config.get_prepare_callback_config()
    prepare_callbacks = PrepareCallback(config=prepare_callbacks_config)
    callback_list = prepare_callbacks.get_tb_ckpt_callbacks()

    training_config = config.get_training_config()
    training = Training(config=training_config)
    training.get_base_model()
    training.get_tokenizer()
    training.train_valid_generator()
    training.train()

except Exception as e:
    raise e

