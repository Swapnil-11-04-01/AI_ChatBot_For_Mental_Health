import pickle
from pathlib import Path
import pandas as pd
import re
from nltk.stem import PorterStemmer
from EVE_AI.entity.config_entity import (TrainingConfig)
import warnings

warnings.filterwarnings("ignore")

class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_base_model(self):
        with open(self.config.base_model_path, 'rb') as f:
            self.model = pickle.load(f)

    def get_tokenizer(self):
        with open(self.config.base_tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)


    @staticmethod
    def preprocess_text(text):
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = text.lower()
        text = text.split()
        text = [PorterStemmer().stem(word) for word in text]
        text = " ".join(text)
        return text

    @staticmethod
    def save_model(path: Path, model):
        with open(path, 'wb') as f:
            pickle.dump(model, f)

    def train_valid_generator(self):
        self.training_data_frame = pd.read_csv(self.config.training_data)
        self.train_text_generator = self.training_data_frame.iloc[:,0]
        self.train_text_generator = self.train_text_generator.apply(self.preprocess_text)
        self.train_labels_generator = self.training_data_frame.iloc[:,1]

        self.validation_data_frame = pd.read_csv(self.config.validation_data)
        self.valid_text_generator = self.validation_data_frame.iloc[:,0]
        self.valid_text_generator = self.valid_text_generator.apply(self.preprocess_text)
        self.valid_labels_generator = self.validation_data_frame.iloc[:,1]

    def train(self):
        self.save_model(path=self.config.preprocessor_path, model=self.preprocess_text)
        self.tokenized_training_data = self.tokenizer.fit_transform(self.train_text_generator.tolist())
        self.train_features = self.tokenized_training_data.toarray()

        self.save_model(path=self.config.fitted_tokenizer_path, model=self.tokenizer)

        self.tokenized_validation_data = self.tokenizer.transform(self.valid_text_generator.tolist())
        self.valid_features = self.tokenized_validation_data.toarray()

        self.train_labels = self.train_labels_generator
        self.valid_labels = self.valid_labels_generator

        self.model.fit(self.train_features,
                       self.train_labels,
                       eval_set=(self.valid_features, self.valid_labels),
                       verbose=self.config.params_verbose)

        self.save_model(path=self.config.trained_model_path, model=self.model)