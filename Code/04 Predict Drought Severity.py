import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

import pickle

import streamlit as st 

import requests
import io

import warnings
warnings.filterwarnings('ignore')

path = 'https://storage.googleapis.com/cropsafe-drought-prediction-data-store/'

model = 'model/random_forest_model_v3.pkl'

pickle_file_url = 'https://storage.googleapis.com/cropsafe-drought-prediction-data-store/model/random_forest_model_v3.pkl'
response = requests.get(pickle_file_url)
response.raise_for_status()

loaded_model = pickle.loads(response.content)

#loaded_model = pickle.load(open('', 'rb'))

fips_master = pd.read_csv(path + 'data/state_and_county_fips_master.csv')

predictors = ['RH', 'WS50M_RANGE', 'DTR', 'WS10M_RANGE', 'aspectS', 'Wind_Chill', 'Std_T2M', 'WS50M', 'elevation', 'Pressure_Variation', 'T2M_MAX', 'ET', 'Heat_Index', 'PRECTOT', 'Cumulative_Precip', 'year', 'month', 'Dry_Days_Sequence']

def main(): 
    st.title("Predict Drought Severity")
    st.markdown("""You can use this tool to predict drought severity level of a county by entering its meteorological and topographical characteristics below.""", unsafe_allow_html = True)
    
    county_fips = st.text_input("County FIPS", "0")
    var1 = st.text_input("RH", "0")
    var2 = st.text_input("WS50M_RANGE","0") 
    var3 = st.text_input("DTR: ","0") 
    var4 = st.text_input("WS10M_RANGE","0") 
    var5 = st.text_input("aspectS","0") 
    var6 = st.text_input("Wind_Chill","0") 
    var7 = st.text_input("Std_T2M","0") 
    var8 = st.text_input("WS50M","0") 
    var9 = st.text_input("elevation","0") 
    var10 = st.text_input("Pressure_Variation","0") 
    var11 = st.text_input("T2M_MAX","0") 
    var12 = st.text_input("ET","0") 
    var13 = st.text_input("Heat_Index","0") 
    var14 = st.text_input("PRECTOT","0") 
    var15 = st.text_input("Cumulative_Precip","0") 
    var16 = st.text_input("year","0") 
    var17 = st.text_input("month","0") 
    var18 = st.text_input("Dry_Days_Sequence","0")
    
    county_name = fips_master[fips_master['fips'] == int(county_fips)]['name'].unique()[0]
    state_name = fips_master[fips_master['fips'] == int(county_fips)]['state'].unique()[0]
    
    if st.button("Predict"): 
        features = [predictors]
        data = {'RH': float(var1),
                'WS50M_RANGE': float(var2),
                'DTR': float(var3),
                'WS10M_RANGE': float(var4),
                'aspectS': float(var5),
                'Wind_Chill': float(var6),
                'WS50M': float(var7),
                'Std_T2M': float(var8),
                'elevation': float(var9),
                'Pressure_Variation': float(var10),
                'T2M_MAX': float(var11),
                'ET': float(var12),
                'Heat_Index': float(var13),
                'PRECTOT': float(var14),
                'Cumulative_Precip': float(var15),
                'year': float(var16),
                'month': float(var17),
                'Dry_Days_Sequence': float(var18)}
        print(data)
        df = pd.DataFrame([list(data.values())], columns = predictors)
                      
        prediction = loaded_model.predict(df[predictors])
    
        output = prediction[0]

        st.success(f'Drought severity level at {county_name}, {state_name} is {output}')
        
if __name__=='__main__': 
    main()