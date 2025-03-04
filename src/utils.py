import os
import sys
from src.exception import CustomException
from src.logger import logging
import pickle
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path,object):
    try:
        logging.info("Entered the save object method")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file:
            dill.dump(object,file)
        logging.info("Object saved successfully")
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        logging.info("Entered the evaluate model method")
        model_report = {}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            param=params[list(models.keys())[i]]
            gs = GridSearchCV(model,param,cv=3)
            gs.fit(X_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            model_report[list(models.keys())[i]]=test_model_score
        logging.info("Model evaluation completed successfully")
        return model_report
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        logging.info("Entered the load object method")
        with open(file_path,'rb') as file:
            return pickle.load(file)
        logging.info("Object loaded successfully")
    except Exception as e:
        raise CustomException(e,sys)


