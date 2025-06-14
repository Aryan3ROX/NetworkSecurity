from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(self.training_pipeline_config)
            logging.info('Start Data Ingestion')
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info('Data Ingestion Completed')
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = DataValidationConfig(self.training_pipeline_config)
            logging.info('Start Data validation')
            data_validation = DataValidation(data_ingestion_artifact,self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info('Data Validation Completed')
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
      
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(self.training_pipeline_config)
            logging.info('Start Data Transformation')
            data_transformation = DataTransformation(data_validation_artifact,self.data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info('Data Transformation Completed')
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
      
    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact):
        model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        logging.info('Initiate the model training')
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        return model_trainer_artifact
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_training_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            return model_training_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)