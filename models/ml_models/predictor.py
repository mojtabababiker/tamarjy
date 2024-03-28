#!/usr/bin/env python3
"""
The machine learning models interface, which wrap the NLP
models and the disease predictor with the application
"""
import json
import os.path
import pickle
import numpy as np
import spacy


class Predictor:
    """Machine Learning Models interface, used to get the disease
     predictions from the user text using the NLP model and the
     disease prediction model"""
    def __init__(self):
        """Initiate the Predictor class"""
        _dirname = os.path.dirname(__file__)
        self.__nlp = spacy.load(os.path.join(_dirname, 'custom_ner'))
        # setup the NLP model
        roller = self.__nlp.add_pipe("entity_ruler", after="ner",
                                     config={"validate": True, "overwrite_ents": True})

        with open(
            os.path.join(_dirname, 'custom_ner', 'symptoms_patterns.json'),
            'r', encoding='utf-8') as f:
            symptoms_patterns = json.load(f)

        roller.add_patterns(symptoms_patterns)

        # load the disease prediction model
        _path = os.path.join(_dirname, 'ml_predictor', 'predictor.pkl')
        with open(_path, 'rb') as f:
            self.__model = pickle.load(f)

        # define instance variables for operational uses
        self.extracted_symptoms = []
        with open(
            os.path.join(_dirname, 'ml_predictor', 'symptoms_synonymous.pkl'),
            'rb') as f:
            self.__symptoms_synonyms = pickle.load(f)

    def predict(self, text:str="") -> dict:
        """
        receive the text from the application and run all the needed
        process on it by calling the NLP model and return a 
        dictionary that represents the predicted diseases.
        parameters:
        ------------
        text: str, the text input contains the user symptoms

        return:
        -------------
        predictions: dict, key, value pairs represents the predicted 
                     disease and its probability
        """
        if not text or not isinstance(text, str):
            return {}
        doc = self.__nlp(text)
        symptoms = [ent.text.replace(' ', '_') for ent in doc.ents
                    if ent.label_ == "MedicalCondition"]
        self.extracted_symptoms = symptoms  # for the external use
        if not symptoms:
            return {}
        symptoms_array = self.__process_symps(symptoms)
        result = self.__model.predict_proba(symptoms_array)[0]
        predictions = self.__enhance_prediction(result)
        return predictions

    def __process_symps(self, symptoms:list):
        """Process the list of symptoms by getting the predefined
        ones that equivalent to the symptoms on the symptoms list

        parameters:
        -------------
        symptoms: list, the list of the symptoms entities

        return:
        --------------
        a numpy array with the processed symptoms
        """
        # set the logic of finding the synonymous of the
        # predefined symptoms on the symptoms list
        for idx, symp in enumerate(symptoms):
            for key, value in self.__symptoms_synonyms.items():
                if symp in value:
                    symptoms[idx] = key
                    break
        symptoms_array = []
        for symp in self.__model.feature_names_in_:
            if symp in symptoms:
                symptoms_array.append(1)
            else:
                symptoms_array.append(0)
        symptoms_array = np.array(symptoms_array).reshape(1, -1)
        return symptoms_array

    def __enhance_prediction(self, result, tol:float=0.15) -> dict:
        """Get the top predicted disease based on their probabilities and the tolerance (tol).

        Args:
            result (numpy.ndarray): The array of predicted disease probabilities.
            tol (float, optional): The tolerance level for selecting the top diseases.
                                   Defaults to 0.15.

        Returns:
            dict: A dictionary containing the top predicted diseases and their probabilities.
        """
        predictions = dict()
        top_diseases_index = np.where(result >= tol)[0]
        try:
            neg_prob = (1 - (result[top_diseases_index].sum())) / len(top_diseases_index)
            for idx in top_diseases_index:
                disease = self.__model.classes_[idx]
                disease_prob = round((result[idx] + neg_prob) * 100, 2)
                if disease_prob >= 85.0:
                    disease_prob = round((result[idx]) * 100, 2)
                predictions[disease] = disease_prob
        except Exception:
            # log it
            return {}
        # if the selected sensitivity (tol) was too high for the current symptoms
        if not predictions or len(predictions) <= 2:
            # recursively call the method with tol - the prob of one disease (0.0076)
            predictions = self.__enhance_prediction(result, tol=tol - 0.008)
        return predictions
