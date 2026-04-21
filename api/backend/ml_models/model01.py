"""
model01.py demonstrates how to store model parameters in the database
and retrieve them at prediction time via a REST route.
"""
import numpy as np
from flask import current_app
from backend.db_connection import get_db


def train():
    """
    Placeholder for a training routine. Could be triggered from an
    admin route to retrain the model and store new parameters in the DB.
    """
    return 'Training the model'


def test():
    return 'Testing the model'


def predict(var01, var02):
    """
    Retrieves model parameters from the database and uses them for
    real-time prediction. Parameters are stored as a comma-separated
    string and parsed into a numpy array here.
    """
    cursor = get_db().cursor(dictionary=True)
    try:
        query = 'SELECT beta_vals FROM model1_params ORDER BY sequence_number DESC LIMIT 1'
        cursor.execute(query)
        params = cursor.fetchone()['beta_vals']

        # Parse the stored parameter string (e.g. "[1.2,3.4,5.6]") into a numpy array
        params_array = np.array(list(map(float, params[1:-1].split(','))))
        current_app.logger.info(f'params_array = {params_array}')

        # Prepend 1.0 as the intercept term, then dot with the parameter vector
        input_array = np.array([1.0, float(var01), float(var02)])
        return np.dot(params_array, input_array)
    finally:
        cursor.close()
