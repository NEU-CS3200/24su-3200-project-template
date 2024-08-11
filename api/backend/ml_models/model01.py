"""
model01.py is an example of how to access model parameter values that you are storing
in the database and use them to make a prediction when a route associated with prediction is
accessed. 
"""

from backend.db_connection import db
import numpy as np
import logging


def train():
    """
    You could have a function that performs training from scratch as well as testing (see below).
    It could be activated from a route for an "administrator role" or something similar.
    """
    return "Training the model"


def test():
    return "Testing the model"


def predict(var01, var02):
    """
    Retreives model parameters from the database and uses them for real-time prediction
    """
    # get a database cursor
    cursor = db.get_db().cursor()
    # get the model params from the database
    query = "SELECT beta_vals FROM model1_params ORDER BY sequence_number DESC LIMIT 1"
    cursor.execute(query)
    return_val = cursor.fetchone()

    params = return_val["beta_vals"]
    logging.info(f"params = {params}")
    logging.info(f"params datatype = {type(params)}")

    # turn the values from the database into a numpy array
    params_array = np.array(list(map(float, params[1:-1].split(","))))
    logging.info(f"params array = {params_array}")
    logging.info(f"params_array datatype = {type(params_array)}")

    # turn the variables sent from the UI into a numpy array
    input_array = np.array([1.0, float(var01), float(var02)])

    # calculate the dot product (since this is a fake regression)
    prediction = np.dot(params_array, input_array)

    return prediction

    ##############################################################

    # # retreive the parameters from the appropriate table
    # cursor.execute('select beta_0, beta_1, beta_2 from model1_param_vals')
    # # fetch the first row from the cursor
    # data = cursor.fetchone()
    # # calculate the predicted result using this functions arguments as well as the model parameter values
    # result = data[0] + int(var01) * data[1] + int(var02) * data[2]

    # # return the result
    # return result
