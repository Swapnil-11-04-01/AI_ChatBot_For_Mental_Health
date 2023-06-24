from EVE_AI.config.configuration import ConfigurationManager
from EVE_AI.components.training import Training
from EVE_AI.components.base import Base
from EVE_AI import logger
import warnings

warnings.filterwarnings("ignore")

STAGE_NAME = "Training"

class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training = Training(config=training_config)
        training.get_base_model()
        training.get_tokenizer()
        training.train_valid_generator()
        training.train()

        base_config = config.get_base_config()
        base = Base(config=base_config)
        base.intent_data_modifier(base.intent_data)




if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e