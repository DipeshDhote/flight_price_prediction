import sys
from src.flight_price_prediction.logger import logging
from src.flight_price_prediction.exception import CustomException
from src.flight_price_prediction.components.data_ingestion import DataIngestion,DataIngestionConfig

if __name__=="__main__":
    logging.info("logging has been started")
    try:
        data_ingetion = DataIngestion()
        data_ingetion.initiate_data_ingestion()
        
    
    
    
    
    
    except Exception as e:
        raise CustomException(e,sys)