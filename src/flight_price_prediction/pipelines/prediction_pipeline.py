import os
import sys 
import pandas as pd
import numpy as np
from src.flight_price_prediction.logger import logging
from src.flight_price_prediction.exception import CustomException
from src.flight_price_prediction.utils import load_object 
import datetime



class PredictPipeline:
    
    def __init__(self):
        pass

    def predict(self,features):       
          try:

            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")            
            print("Before Loading")

            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            print("After Loading")

            data_scaled=preprocessor.transform(features)
            preds=model.predict(data_scaled)
            logging.info("input data scaled and model predict completed")
            print(f" The flight price will be :{preds}")
            return preds
            
          except Exception as e:
                raise CustomException(e,sys)




class CustomData:
    def __init__( self,                            
     Airline:str,
     Date_of_Journey:str,
     Source:str,
     Destination:str, 
     Dep_Time:str,
     Arrival_Time:str,
     Total_Stops:float,
     Duration_In_Minutes:int
     ):
     
            
     self.Airline = Airline
     self.Date_of_Journey = Date_of_Journey
     self.Source= Source
     self.Destination = Destination
     self.Dep_Time = Dep_Time
     self.Arrival_Time = Arrival_Time
     self.Total_Stops = Total_Stops
     self.Duration_In_Minutes = Duration_In_Minutes
      

    def get_data_as_data_frame(self):
          try:
            custom_data_input_dict = {                                          
                  'Airline':[self.Airline],
                  'Date_of_Journey':[self.Date_of_Journey],
                  'Source':[self.Source],
                  'Destination':[self.Destination], 
                  'Dep_Time':[self.Dep_Time],
                  'Arrival_Time':[self.Arrival_Time],
                  'Total_Stops':[self.Total_Stops],
                  'Duration_In_Minutes':[self.Duration_In_Minutes]
            }
                
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
                
          except Exception as e:
                raise CustomException(e,sys)
                