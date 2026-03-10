from NetworkSecurity.Compenents.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingstion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingstion_config)
        logging.info("initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)    