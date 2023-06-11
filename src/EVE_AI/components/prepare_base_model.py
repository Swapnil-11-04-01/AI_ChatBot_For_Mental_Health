import pickle
from pathlib import Path
import tensorflow as tf
from transformers import TFDistilBertForSequenceClassification, DistilBertTokenizer
from EVE_AI.entity.config_entity import (PrepareBaseTokenizerConfig, PrepareBaseModelConfig)

class PrepareBaseModel:
    def __init__(self, config_model: PrepareBaseModelConfig, config_tokenizer: PrepareBaseTokenizerConfig):
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