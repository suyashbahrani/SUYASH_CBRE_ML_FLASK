# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit
from flask import request
from apps.config import config_dict
from apps import create_app, db
from prediction import predict_price  # Import the predict_price function
from broker_list import predict_and_get_brokers



# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

# Route to handle predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json 
    print("Helloooo",data)
    # Assuming data is sent in JSON format
    # Extract data from the request
    property_size = data['property_size']
    commission_rate = data['commission_rate']
    difference_days = data['difference_days']
    feedback_score = data['feedback_score']
    property_type = data['property_type']
    transaction_type = data['transaction_type']
    region = data['region']
    country = data['country']
    area = data['area']
    # Make prediction using the predict_price function
    prediction = predict_price(property_size, commission_rate, difference_days, feedback_score,
                               property_type, transaction_type, region, country, area)
    
    df_broker_data = predict_and_get_brokers(property_size, commission_rate, difference_days, feedback_score,
                                              property_type, transaction_type, region, country, area,
                                              prediction)
    
    
    broker_data_dict = df_broker_data.to_dict(orient='records')

    return {'predicted_price': prediction, 'broker_data': broker_data_dict}




if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)
    
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             )
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' )
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT )

if __name__ == "__main__":
    app.run(debug=True)
