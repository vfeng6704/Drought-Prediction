import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

import pickle

import geopandas as gpd

import streamlit as st 
import pydeck as pdk

import plotly.express as px
import plotly.figure_factory as ff

import json

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

#loaded_model = pickle.load(open(path + model, 'rb'))

gdf = gpd.read_file(path + 'data/counties.geojson')
gdf['county_fips'] = gdf['STATEFP'].astype(str) + gdf['COUNTYFP'].astype(str)
gdf['county_fips'] = gdf['county_fips'].astype(int)

predictors = ['RH', 'WS50M_RANGE', 'DTR', 'WS10M_RANGE', 'aspectS', 'Wind_Chill', 'Std_T2M', 'WS50M', 'elevation', 'Pressure_Variation', 'T2M_MAX', 'ET', 'Heat_Index', 'PRECTOT', 'Cumulative_Precip', 'year', 'month', 'Dry_Days_Sequence']


def main(): 
    st.title("Predict Drought Severity")
    st.markdown("### Batch Inference")
    st.markdown("""Upload a batch file containing meteorological and topographical characteristics of US counties across drought prone zones to predict drought severity levels of multiple counties and visualize the trend.""", unsafe_allow_html = True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type = "csv")
    
    if uploaded_file is not None:
        scoring_df = pd.read_csv(uploaded_file)
        st.success(f'Scoring dataset contains {scoring_df.shape[0]} rows and {scoring_df.shape[1]} columns.')
    
    if st.button("Predict"): 
        average_actual_drought_score = scoring_df['score'].mean()
        predictions = loaded_model.predict(scoring_df[predictors])
        scoring_df['Prediction'] = predictions
        scoring_df = scoring_df.groupby('county_fips')['Prediction'].mean().reset_index()
        merged_gdf = gdf.merge(scoring_df, on = 'county_fips')
        merged_gdf = merged_gdf.rename(columns = {'county_fips': 'County FIPS'})
      
        fig = px.choropleth(merged_gdf,
                    geojson = merged_gdf.geometry,
                    locations = merged_gdf.index,
                    color = "Prediction",
                    color_continuous_scale = "sunsetdark")

        fig.update_geos(fitbounds = "locations", visible = True)
        fig.update_layout(margin = {"r": 0, "t": 0, "l": 0, "b": 0}, width = 1000, height = 300)
        
        st.plotly_chart(fig, use_container_width = True)
        
        st.markdown(f'Average actual drought score: **{np.round(average_actual_drought_score, 2)}**')
        st.markdown(f'Average predicted drought score: **{np.round(predictions.mean(), 2)}**')


        
if __name__=='__main__': 
    main()