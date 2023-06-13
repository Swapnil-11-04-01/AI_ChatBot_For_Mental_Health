from sklearn.metrics import f1_score
import pandas as pd
import pickle
from EVE_AI.constants import *
from EVE_AI.utils.common import save_json
from EVE_AI.entity.config_entity import EvaluationConfig
import warnings

warnings.filterwarnings("ignore")

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

        self.preprocessor = self.load_model(self.config.path_of_preprocessor)
        self.tokenizer = self.load_model(self.config.path_of_tokenizer)

        self.X_test = self.test_data.iloc[:, 0]
        self.X_test = self.X_test.apply(self.preprocessor)
        self.X_test = self.tokenizer.transform(self.X_test.tolist()).toarray()
        self.y_test = self.test_data.iloc[:, 1]

    def evaluation(self):
        self.model = self.load_model(self.config.path_of_model)
        self.y_pred = self.model.predict(self.X_test)
        self.score = f1_score(self.y_test, self.y_pred, average='weighted')

    def save_score(self):
        scores = {"accuracy": f'{round(self.score*100, 2)}%'}
        save_json(path=Path("scores.json"), data=scores)