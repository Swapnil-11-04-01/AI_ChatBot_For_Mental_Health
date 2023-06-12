import os
from dataclasses import dataclass
from pathlib import Path
from sklearn.metrics import f1_score
import pandas as pd
import pickle
from EVE_AI.constants import *
from EVE_AI.utils.common import read_yaml, create_directories, save_json


@dataclass(frozen=True)
class EvaluationConfig:
    path_of_model: Path
    path_of_tokenizer: Path
    test_data: Path
    all_params: dict
    params_verbose: int


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=self.config.training.trained_model_path,
            path_of_tokenizer=self.config.prepare_fitted_tokenizer.fitted_tokenizer_path,
            test_data=os.path.join(self.config.data_ingestion.unzip_dir, "test.csv"),
            all_params=self.params,
            params_verbose=self.params.VERBOSE
        )
        return eval_config


from urllib.parse import urlparse


class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config

    @staticmethod
    def load_model(path: Path):
        with open(path, 'rb') as f:
            model = pickle.load(f)
        return model

    def _valid_generator(self):
        self.test_data = pd.read_csv(self.config.test_data)

        self.tokenizer = self.load_model(self.config.path_of_tokenizer)

        self.X_test = self.test_data.iloc[:, 0]
        self.X_test = self.tokenizer.transform(self.X_test.tolist()).toarray()
        self.y_test = self.test_data.iloc[:, 1]

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self.y_pred = self.model.predict(self.X_test)
        self.score = f1_score(self.y_test, self.y_pred, average='weighted')

    def save_score(self):
        scores = {"accuracy": f'{round(self.score*100, 2)}%'}
        save_json(path=Path("scores.json"), data=scores)


try:
    config = ConfigurationManager()
    val_config = config.get_validation_config()
    evaluation = Evaluation(val_config)
    evaluation._valid_generator()
    evaluation.evaluation()
    evaluation.save_score()

except Exception as e:
    raise e