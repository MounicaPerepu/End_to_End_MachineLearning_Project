import os
import sys
import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import logging
import dill

def save_object(file_path,object):
    try:
        logging.info("Entered the save object method")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file:
            dill.dump(object,file)
        logging.info("Object saved successfully")
    except Exception as e:
        raise CustomException(e,sys)



