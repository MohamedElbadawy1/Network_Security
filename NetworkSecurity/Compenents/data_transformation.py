import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from NetworkSecurity.Constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS

from NetworkSecurity.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact

from NetworkSecurity.entity.config_entity import DataTransfromationConfig

from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.utlis.main_utils.utils import save_numpy_array_data, save_object



class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact, 
                 data_transformtation_config: DataTransfromationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config = data_transformtation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def get_data_transformer_object(cls)->Pipeline:
        """
        it initializes a KNNImputer object with the parameters specified in the training_pipeline.py
        file and returns a Pipeline object with the KNNImputer object as the first step.
        """
        logging.info("Entered get_data_transformer_object method of the DataTransformation Class")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            processor = Pipeline([("Imputer", imputer)])
            return processor
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation Method of DataTransformation class")
        try:
            logging.info("Starting Data Transformation")
            
            ## read the train and test dataframe.
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            ## Training dataframe split into features and target
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1,0)

            ## Testing dataframe split into features and target
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1,0)

            ## Processor object
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            ## Save Numpy array data.
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            ## Preparing the artifact.
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifact
        
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)











