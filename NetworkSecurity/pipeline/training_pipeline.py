import os
import sys

from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException

from NetworkSecurity.Compenents.data_ingestion import DataIngestion
from NetworkSecurity.Compenents.data_validation import DataValidation
from NetworkSecurity.Compenents.data_transformation import DataTransformation
from NetworkSecurity.Compenents.model_trainer import ModelTrainer

from NetworkSecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransfromationConfig,
    ModelTrainerConfig
)


from NetworkSecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact, 
    DataTransformationArtifact,
    ModelTrainerArtifact
)


class TrainingPipeline:
    def __init__(self):
        self.train_pipeline_config = TrainingPipelineConfig()


    ## Data Ingestion Init.
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.train_pipeline_config)
            logging.info("\nStart Data Ingestion ...")
            data_ingestion = DataIngestion(self.data_ingestion_config)
            self.data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("=== Data Ingestion Completed ===")
            return self.data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)



    ## Data Validation Init.
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(self.train_pipeline_config)
            logging.info("\nStart Data Validation ...")
            data_validation = DataValidation(data_ingestion_artifact, self.data_validation_config)
            self.data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("=== Data Ingestion Completed ===")
            return self.data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)       



    ## Data Transformation Init.
    def start_data_transforamtion(self, data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransfromationConfig(self.train_pipeline_config)
            logging.info("\nStart Data Transformation ...")
            data_transformation = DataTransformation(data_validation_artifact, self.data_transformation_config)
            self.data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("=== Data Transformation Completed ===")
            return self.data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    ## Model Trainer Init.
    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(self.train_pipeline_config)
            model_trainer = ModelTrainer(self.model_trainer_config, data_transformation_artifact)
            logging.info("\nModel Training Started .. ")
            self.model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("=== Model Training Completed === ")
            return self.model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)  
        

    ## Run the Pipeline
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transforamtion(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)




