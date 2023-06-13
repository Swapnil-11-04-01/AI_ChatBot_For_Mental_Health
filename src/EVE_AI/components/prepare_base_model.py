import pickle
from pathlib import Path
from EVE_AI.entity.config_entity import (PrepareBaseTokenizerConfig, PrepareBaseModelConfig)
from sklearn.feature_extraction.text import TfidfVectorizer
from catboost import CatBoostClassifier
import warnings

warnings.filterwarnings("ignore")

class PrepareBaseModel:
    def __init__(self, config_model: PrepareBaseModelConfig,
                 config_tokenizer: PrepareBaseTokenizerConfig):
        self.config_model = config_model
        self.config_tokenizer = config_tokenizer

    def get_ml_model(self):
        self.model = CatBoostClassifier(iterations=self.config_model.params_iterations,
                                        learning_rate=self.config_model.params_learning_rate,
                                        depth=self.config_model.params_depth,
                                        loss_function='MultiClass')

        self.save_model(path=self.config_model.base_model_path, model=self.model)


    def get_tokenizer(self):
        self.tokenizer = TfidfVectorizer()
        self.save_model(path=self.config_tokenizer.base_tokenizer_path, model=self.tokenizer)


    @staticmethod
    def save_model(path: Path, model):
        with open(path, 'wb') as f:
            pickle.dump(model, f)