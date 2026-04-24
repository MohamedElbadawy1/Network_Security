from NetworkSecurity.Compenents.data_ingestion import DataIngestion
from NetworkSecurity.Compenents.data_validation import DataValidation
from NetworkSecurity.Compenents.data_transformation import DataTransformation
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig,DataTransfromationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        ## test data ingestion
        training_pipeline_config = TrainingPipelineConfig()
        data_ingstion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingstion_config)
        logging.info("initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")

        ## test data validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        

        ## test data transformation
        data_transformation_config = DataTransfromationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info("Initiate the Data Transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e,sys)    