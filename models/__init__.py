"""
Description: This file initializes the storage variable and 
reloads the data from the database.
"""
from models.engine.db_storage import DatabaseStorage
from models.ml_models.predictor import Predictor

storage = DatabaseStorage() # create an instance of the DatabaseStorage class
storage.reload() # reload the data from the database
predictor = Predictor() # create an instance of the machine learning Predictor class
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f' # set the time format
