
import sys
from src.flight_price_prediction.logger import logging
from src.flight_price_prediction.exception import CustomException
from src.flight_price_prediction.components.data_ingestion import DataIngestion
from src.flight_price_prediction.components.data_transformation import DataTransformation
from flight_price_prediction.components.model_trainer import ModelTrainer
from src.flight_price_prediction.components.data_ingestion import DataIngestion
from src.flight_price_prediction.components.data_transformation import DataTransformation

if __name__=="__main__":
    logging.info("logging has been started")
    try:
        # Data Ingestion
        data_ingetion = DataIngestion()
        train_data_path,test_data_path = data_ingetion.initiate_data_ingestion()
        
        # # Data Transformation
        data_transformation = DataTransformation()
        train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data_path,test_data_path)

        # # Model Trainer
        model_trainer = ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr,test_arr))
     
    except Exception as e:
        raise CustomException(e,sys)

