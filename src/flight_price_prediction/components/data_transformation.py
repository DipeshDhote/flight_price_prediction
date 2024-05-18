import  sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler,OneHotEncoder,MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from feature_engine.datetime import DatetimeFeatures

from src.flight_price_prediction.logger import logging
from src.flight_price_prediction.exception import CustomException
import os

from src.flight_price_prediction.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This fuction responsible for data transformation
        '''
        try:
            # defining numerical columns
            numerical_columns =["Total_Stops" ,"Duration_In_Minutes"]   

            # defining categorical columns
            categorical_columns =["Airline", "Source", "Destination"]

            # defining date columns 
            date_col = ["Date_of_Journey"]

            # defining time column
            time_col = ["Dep_Time","Arrival_Time"]



            # making pipeline for numerical columns
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("Scaler", StandardScaler())
                ]
            )
             
            # making pipeline for categorical columns
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehotencoder", OneHotEncoder())
                ]
            )
            
            # making pipeline for date columns 
            date_pipeline = Pipeline(
                steps=[
                    ("date",DatetimeFeatures(features_to_extract= ["month", "week", "day_of_week", "day_of_year"], yearfirst=True, format="mixed")),
                    ("minmaxscaling", MinMaxScaler())
                ]
            )

           
           # making pipeline for time columns 
            time_pipeline = Pipeline(
                steps=[
                    ("dt",DatetimeFeatures(features_to_extract= ["hour","minute"],format="mixed")),
                    ("minmaxscaling", MinMaxScaler())
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")
            logging.info(f"Date columns: {date_col}")
            logging.info(f"Time columns: {time_col}")

            logging.info("pipeline for numerical column completed")

            preprocessor = ColumnTransformer(
                
                [   
                  ("NumericalPipeline", num_pipeline, numerical_columns),
                  ("CategoricalPipeline", cat_pipeline, categorical_columns),
                  ("DatePipeline", date_pipeline, date_col),
                  ("TimePipeline", time_pipeline, time_col)
                ]
            )
            logging.info("column transformation completed")
            
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_transformation(self,train_path,test_path):

        try:

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)


            logging.info("Reading train and test file")

            preprocessing_obj = self.get_data_transformer_object()
           
            target_column_name="Price" 
        
        
            # divide the train dataset to independent and dependent features

            input_features_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]
            
                       
            # divide the test dataset to independent and dependent features

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]
                
            logging.info("Applying preprocessing on training and test dataframe")
            print(type(input_features_train_df))
            print(target_feature_train_df)

            input_feature_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            

            logging.info("preprocessing is completed")

            train_arr = np.c_[        
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (

                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )


        except Exception as e:
            raise CustomException(e,sys)




            