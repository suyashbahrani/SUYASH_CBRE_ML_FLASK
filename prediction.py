import pandas as pd
import joblib

# Function to make predictions using the trained model
def predict_price(property_size, commission_rate, difference_days, feedback_score,
                  property_type, transaction_type, region, country, area):
    # Load the preprocessor and regressor
    model = joblib.load('model2.pkl')

    # Create a DataFrame with the input parameters
    input_data = pd.DataFrame({
        'Property_Size': [property_size],
        'Commission_Rate': [commission_rate],
        'Difference (in days)': [difference_days],
        'Feedback_Score': [feedback_score],
        'Property_Type': [property_type],
        'Transaction_Type': [transaction_type],
        'Region': [region],
        'Country': [country],
        'Area': [area]
    })

    # Make predictions on the input data
    prediction = model.predict(input_data)

    return prediction[0]



 