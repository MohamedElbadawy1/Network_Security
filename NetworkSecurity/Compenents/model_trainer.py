import os
import pandas as pd
import numpy as np
import sys
import mlflow

from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException

from NetworkSecurity.entity.config_entity import ModelTrainerConfig
from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from NetworkSecurity.utlis.main_utils.utils import save_object, load_object, load_numpy_array_data,evaluate_model
from NetworkSecurity.utlis.ml_utils.metric.classification_metric import get_classification_score
from NetworkSecurity.utlis.ml_utils.model.estimator import NetworkModel

from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)


class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def track_mlflow(self, best_model, classification_metric):
    
        # 2. Give your experiment a name so it's easy to find
        mlflow.set_experiment("Network_Security_Model_Training")

        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.percision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)

            mlflow.sklearn.log_model(best_model, "Model")

    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradiant Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }
        params = {
            "Random Forest": {
                "n_estimators": [100, 200],
                #"max_depth": [None, 10],
                #"min_samples_split": [2, 5],
                #"max_features": ["sqrt"]
            },
            "Decision Tree":{
                "max_depth": [None, 10, 20],
                #"min_samples_split": [2, 5],
                #"min_samples_leaf": [1, 2]
            },
            "Gradiant Boosting": {
                "n_estimators": [100, 200],
                "learning_rate": [0.05, 0.1],
                "max_depth": [3, 5],
                #"subsample": [0.8, 1.0]
            },
            "Logistic Regression": {
                "C": [0.1, 1, 10],
                "penalty": ["l2"],
                "solver": ["lbfgs"],
                #"max_iter": [200]
            },
            "AdaBoost": {
                "n_estimators": [50, 100],
                "learning_rate": [0.5, 1.0]
            }
        }

        model_report:dict = evaluate_model(x_train, y_train, x_test, y_test, models, params)
        
        ## Get the best model name and score.
        best_model_name = max(model_report, key=model_report.get)
        best_model_score = model_report[best_model_name]

        logging.info(f"best model is {best_model_name} with score: {best_model_score}")
        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)
        y_test_pred = best_model.predict(x_test)

        classification_train_mertric = get_classification_score(y_train, y_train_pred)
        classification_test_mertric = get_classification_score(y_test, y_test_pred)

        ## Track the MLFlow
        self.track_mlflow(best_model, classification_train_mertric) # track for train
        self.track_mlflow(best_model, classification_test_mertric) # track for test

        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocessor, best_model)
        save_object(self.model_trainer_config.trained_model_file_path, network_model)
        save_object("final_models/model.pkl", best_model)
        save_object("final_models/preprocessor.pkl", preprocessor)

        ## Model Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(self.model_trainer_config.trained_model_file_path,
                            classification_train_mertric,
                            classification_test_mertric)
        
        logging.info(f"model Trainer Artifact {model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            import dagshub

            dagshub.init(
            repo_owner='MohamedElbadawy1',
            repo_name='Network_Security',
            mlflow=True
        )
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path
            
            ## loading train and test data
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            ## feature and target for train and test split
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr [:, :-1],
                test_arr [:, -1],
            )

            ## Train the model 
            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)










