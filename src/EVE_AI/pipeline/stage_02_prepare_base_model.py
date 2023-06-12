from EVE_AI.config.configuration import ConfigurationManager
from EVE_AI.components.prepare_base_model import PrepareBaseModel
from EVE_AI import logger
import warnings

warnings.filterwarnings("ignore")

STAGE_NAME = "Prepare base model"

class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()

        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_tokenizer_config = config.get_prepare_base_tokenizer_config()

        prepare_base_model = PrepareBaseModel(config_model=prepare_base_model_config,
                                              config_tokenizer=prepare_base_tokenizer_config)

        prepare_base_model.get_ml_model()
        prepare_base_model.get_tokenizer()





if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e