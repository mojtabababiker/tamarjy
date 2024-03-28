#!/usr/bin/env python3
""" a unittest module for testing the predictor model using unittest
"""

import unittest
from models.ml_models.predictor import Predictor


class TestPredictor(unittest.TestCase):
    """Test class for the ML models prediction using TestCase class
        from unittest module
    """
    @classmethod
    def setUpClass(cls):
        """Setup the test class"""
        cls.predictor = Predictor()
        
    def test_initiate(self):
        """Test the Predictor initiates"""
        self.assertIsInstance(self.predictor, Predictor)

    def test_predict(self):
        """Test the Predictor predict method on normal case
        """
        text = "I was shivering with chills, suffering from high fever, \
            vomiting, headache, nausea, diarrhea, and muscles pain"
        result = self.predictor.predict(text)
        # test the return type
        self.assertIsInstance(result, dict)
        # test the return values
        self.assertTrue('Malaria' in result.keys())

    def test_predict_no_text(self):
        """Test the Predictor predict method with no text
        provided"""
        result = self.predictor.predict()
        # test the return type
        self.assertIsInstance(result, dict)
        # test the return value
        self.assertEqual(len(result), 0)

    def test_predict_no_symptoms(self):
        """Test the Predictor predict method with text
        that have no symptoms in it"""
        text = "The big brown fox, jumped over the little chicken"
        result = self.predictor.predict(text=text)
        # test the return type
        self.assertIsInstance(result, dict)
        # test the return value
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()