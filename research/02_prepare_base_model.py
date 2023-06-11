import pickle
from dataclasses import dataclass
from EVE_AI.constants import *
from EVE_AI.utils.common import read_yaml, create_directories
import urllib.request as request
import zipfile
from EVE_AI import logger
from EVE_AI.utils.common import get_size
import tensorflow as tf
from transformers import TFDistilBertForSequenceClassification, DistilBertTokenizer

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


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config_model = self.config.prepare_base_model

        create_directories([config_model.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config_model.root_dir),
            base_model_path=Path(config_model.base_model_path),
            updated_base_model_path=Path(config_model.updated_base_model_path),
            params_learning_rate=self.params.LEARNING_RATE,
            params_classes=self.params.CLASSES,
            params_batch_size=self.params.BATCH_SIZE,
            params_epochs=self.params.EPOCHS,
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


class PrepareBaseModel:
    def __init__(self, config_model: PrepareBaseModelConfig, config_tokenizer: PrepareBaseModelConfig):
        self.config_model = config_model
        self.config_tokenizer = config_tokenizer

    def get_base_model(self):
        self.model = TFDistilBertForSequenceClassification.from_pretrained(
            'distilbert-base-uncased'
        )

        self.tokenizer = DistilBertTokenizer.from_pretrained(
            'distilbert-base-uncased'
        )

        self.save_model(path=self.config_model.base_model_path, model=self.model)
        self.save_model(path=self.config_tokenizer.base_tokenizer_path, model=self.tokenizer)

    @staticmethod
    def _prepare_full_model(model, classes, freeze_all, freeze_till, learning_rate):
        if freeze_all:
            for layer in model.layers:
                model.trainable = False
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                model.trainable = False

        model.summary()

        # Define the sentiment analysis model based on DistilBERT
        input_ids = tf.keras.Input(shape=(None,), dtype=tf.int32, name='input_ids')
        attention_mask = tf.keras.Input(shape=(None,), dtype=tf.int32, name='attention_mask')

        distilbert_output = model.distilbert([input_ids, attention_mask])

        full_model = tf.keras.Model(inputs=[input_ids, attention_mask], outputs=distilbert_output)

        # Modify the output layer for 6 emotions
        full_model.layers[-1].activation = tf.keras.activations.softmax
        full_model.layers[-1].units = classes
        full_model.layers[-1].kernel_initializer = tf.keras.initializers.TruncatedNormal(stddev=0.02)

        # Compile the model
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        metrics = ['accuracy']
        full_model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

        full_model.summary()
        return full_model

    def update_base_model(self):
        self.full_model = self._prepare_full_model(
            model=self.model,
            classes=self.config_model.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config_model.params_learning_rate
        )

        self.save_model(path=self.config_model.updated_base_model_path, model=self.full_model)

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        with open(path, 'wb') as f:
            pickle.dump(model, f)


try:
    config = ConfigurationManager()

    prepare_base_model_config = config.get_prepare_base_model_config()
    prepare_base_tokenizer_config = config.get_prepare_base_tokenizer_config()

    prepare_base_model = PrepareBaseModel(config_model=prepare_base_model_config,
                                          config_tokenizer=prepare_base_tokenizer_config)

    prepare_base_model.get_base_model()
    prepare_base_model.update_base_model()
except Exception as e:
    raise e