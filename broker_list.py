import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import joblib


df = pd.read_excel('Sample_Data_80K_V5.xlsx')

broker_id_mapping = {firm: id for id, firm in enumerate(df['Broker_Firm_Name'].unique(), start=201)}
# Map the Broker ID to each row in the DataFrame
df['Broker_ID'] = df['Broker_Firm_Name'].map(broker_id_mapping)

import numpy as np

na_values = df['Difference (in days)'].isna()

# Find infinite values
inf_values = ~np.isfinite(df['Difference (in days)'])

# Combine both NA and infinite values
non_finite_values = df[na_values | inf_values]

# Count the number of NA or infinite values
num_non_finite_values = non_finite_values.shape[0]

# Convert Commission_Rate from percentage to decimal
# df['Commission_Rate'] = df['Commission_Rate'] / 100

df['Date_of_Purchase'] = pd.to_datetime(df['Date_of_Purchase'])
df['Date_of_Closing'] = pd.to_datetime(df['Date_of_Closing'])

# Calculate the difference in days
df['Difference (in days)'] = (df['Date_of_Closing'] - df['Date_of_Purchase']).dt.days

# Identify rows with negative differences
negative_difference = df['Difference (in days)'] < 0

# Swap 'Date_of_Purchase' and 'Date_of_Closing' where necessary
temp_dates = df.loc[negative_difference, 'Date_of_Purchase'].copy()
df.loc[negative_difference, 'Date_of_Purchase'] = df.loc[negative_difference, 'Date_of_Closing']
df.loc[negative_difference, 'Date_of_Closing'] = temp_dates

# Recalculate the difference in days after potential swapping
df['Difference (in days)'] = (df['Date_of_Closing'] - df['Date_of_Purchase']).dt.days




# Create a new column 'Price_with_Commission'
df['Price_with_Commission'] = df['Price_in_USD'] * (1 + df['Commission_Rate']/100)
df = df[['Broker_ID', 'Broker_Firm_Name', 'Category', 'Region' , 'Country', 'Area', 'Zipcode', 'Property_Type', 'Property_Size',
         'Transaction_Type', 'Price_in_USD', 'Commission_Rate', 'Price_with_Commission','Date_of_Purchase', 'Date_of_Closing', 'Difference (in days)',
         'Feedback_Score', 'Feedback_Comments', 'Payment_Terms', 'Warranty_Period']]

df['Broker_Firm_Name'] = df['Broker_Firm_Name'].astype(str)
df['Category'] = df['Category'].astype(str)
df['Region'] = df['Region'].astype(str)
df['Country'] = df['Country'].astype(str)
df['Area'] = df['Area'].astype(str)
df['Zipcode'] = df['Zipcode'].astype(str)
df['Property_Type'] = df['Property_Type'].astype(str)
df['Transaction_Type'] = df['Transaction_Type'].astype(str)
df['Price_in_USD'] = df['Price_in_USD'].astype(float)
df['Commission_Rate'] = df['Commission_Rate'].astype(float)
df['Price_with_Commission'] = df['Price_with_Commission'].astype(float)
df['Date_of_Purchase'] = pd.to_datetime(df['Date_of_Purchase'])
df['Date_of_Closing'] = pd.to_datetime(df['Date_of_Closing'])
df['Difference (in days)'] = df['Difference (in days)'].astype(int)
df['Feedback_Score'] = df['Feedback_Score'].astype(float)
df['Feedback_Comments'] = df['Feedback_Comments'].astype(str)
df['Payment_Terms'] = df['Payment_Terms'].astype(str)
df['Warranty_Period'] = df['Warranty_Period'].astype(str)

df['Price_in_USD'] = df['Price_in_USD'] / 1e6  # Divide by 1 million to convert to millions

# Optionally, you can round the values to a certain number of decimal places
# For example, rounding to 2 decimal places:
df['Price_in_USD'] = df['Price_in_USD']


df['Price_with_Commission'] = df['Price_with_Commission'] / 1e6  # Divide by 1 million to convert to millions

# Optionally, you can round the values to a certain number of decimal places
# For example, rounding to 2 decimal places:
df['Price_with_Commission'] = df['Price_with_Commission']

df['Property_Size'] = df['Property_Size'].str.extract('(\d+)').astype(float)

def predict_and_get_brokers(property_size, commission_rate, difference_days, feedback_score,
                            property_type, transaction_type, region, country, area, threshold=0.5):
    # Filter brokers based on the specified conditions
    matched_brokers = df[
        (df['Region'] == region) &
        (df['Country'] == country) &
        (df['Transaction_Type'] == transaction_type) &
        (df['Property_Type'] == property_type) 
        # &
        #(df['Property_Size'].between(property_size * (1 - threshold), property_size * (1 + threshold))) 
        # &
        # (df['Feedback_Score'].between(feedback_score * (1 - threshold), feedback_score * (1 + threshold))) &
        # (df['Commission_Rate'].between(commission_rate * (1 - threshold), commission_rate * (1 + threshold))) &
        # (df['Difference (in days)'].between(difference_days * (1 - threshold), difference_days * (1 + threshold)))
    ]
    # the parameters which i will pass to predict_and_get_brokers

    # Sort the DataFrame by 'Price_with_Commission' and 'Price_in_USD' in ascending order
    df_sorted = matched_brokers.sort_values(by=['Price_with_Commission'])
    # Keep only the first occurrence of each unique broker firm
    unique_brokers_df = df_sorted.drop_duplicates(subset='Broker_Firm_Name', keep='first')
    unique_brokers_df['Price_in_USD'] *= 1e6
    unique_brokers_df['Price_with_Commission'] *= 1e6


    # Sort the DataFrame by multiple columns in descending order of efficiency
    unique_brokers_df = unique_brokers_df.sort_values(by=['Property_Size', 'Price_with_Commission', 'Feedback_Score', 'Difference (in days)'], ascending=[False, True, False, True])

    # Display the sorted DataFrame
   
    
    return unique_brokers_df

