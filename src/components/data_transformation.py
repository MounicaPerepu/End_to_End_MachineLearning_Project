import sys
import os
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_ob_file_path:str=os.path.join('artifacts','preprocessor.pkl') #pkl(pickle) file to store the preprocessor object

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            logging.info("Entered the Data Transformation method or component")
            numerical_columns=["writing_score","reading_score"]
            categorical_columns=["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]

            numerical_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("standard_scaler",StandardScaler(with_mean=False))
            ])
            logging.info("Numerical columns scaling completed")
            categorical_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder(handle_unknown="ignore")),
                ("standard_scaler",StandardScaler(with_mean=False))
            ])
            logging.info("Categorical columns encoding completed")
            preprocessor=ColumnTransformer(transformers=[
                ("numerical_pipeline",numerical_pipeline,numerical_columns),
                ("categorical_pipeline",categorical_pipeline,categorical_columns)
            ])
            logging.info("Preprocessor object created successfully")
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:
            train_df=pd.read_csv(train_data_path)
            test_df=pd.read_csv(test_data_path)
            logging.info("Read the train and test data as dataframe")

            logging.info("Initiating the preprocessor object")
            preprocessor=self.get_data_transformer_object()
            target_column_name="math_score"

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            logging.info("Preprocessor object initiated successfully for train and test data")

            input_feature_train_array=preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_array=preprocessor.transform(input_feature_test_df)

            train_array = np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_array = np.c_[input_feature_test_array,np.array(target_feature_test_df)]
            logging.info("Data transformation saved successfully")

            save_object(
                file_path=self.data_transformation_config.preprocessor_ob_file_path,
                object=preprocessor
            )
            return train_array,test_array,self.data_transformation_config.preprocessor_ob_file_path
        except Exception as e:
            raise CustomException(e,sys)