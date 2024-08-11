import streamlit as st 
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['figure.figsize'] = [10, 5]
plt.rcParams['patch.linewidth'] = 0
plt.rcParams['patch.edgecolor'] = 'none'
color_code = '#CB453E'
import json
import warnings
warnings.filterwarnings('ignore')

path = 'https://storage.googleapis.com/cropsafe-drought-prediction-data-store/'

df = pd.read_csv(path + 'data/drought_dataset_sample_streamlit.csv')
features_description = pd.read_csv(path + 'data/feature_list.csv', encoding = 'unicode_escape')

predictors = [
'PRECTOT',
'PS',
'QV2M',
'T2M',
'T2MDEW',
'T2MWET',
'T2M_MAX',
'T2M_MIN',
'T2M_RANGE',
'TS',
'WS10M',
'WS10M_MAX',
'WS10M_MIN',
'WS10M_RANGE',
'WS50M',
'WS50M_MAX',
'WS50M_MIN',
'WS50M_RANGE',
'Humidex',
'RH',
'Heat_Index',
'Wind_Chill',
'DTR',
'Pressure_Variation',
'Avg_WS10M',
'Gust_Factor',
'ET',
'Cumulative_Precip',
'Dry_Day',
'Dry_Days_Sequence',
'Std_T2M',
'PTHI',
'elevation',
'slope1',
'slope2',
'slope3',
'slope4',
'slope5',
'slope6',
'slope7',
'slope8',
'aspectN',
'aspectE',
'aspectS',
'aspectW',
'aspectUnknown',
'WAT_LAND',
'NVG_LAND',
'URB_LAND',
'GRS_LAND',
'FOR_LAND',
'CULTRF_LAND',
'CULTIR_LAND',
'CULT_LAND',
'SQ1',
'SQ2',
'SQ3',
'SQ4',
'SQ5',
'SQ6',
'SQ7',
'Topographic_Diversity',
'Land_Cover_Diversity',
'Agricultural_Intensity',
'Urban_Rural_Ratio',
'NVG_Veg_Ratio',
'Weighted_SQI',
'Irrigated_Agri_Ratio']

gdf = gpd.read_file(path + 'data/counties.geojson')
gdf['county_fips'] = gdf['STATEFP'].astype(str) + gdf['COUNTYFP'].astype(str)
gdf['county_fips'] = gdf['county_fips'].astype(int)


def main(): 
    
    st.title("About Drought Predictors")
    column_name = st.selectbox('Select a Drought Predictor', predictors)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        selection1 = st.multiselect('Select County', ['Select All'] + list(df['county'].unique()))

    with col2:
        selection2 = st.multiselect('Select State', ['Select All'] + list(df['state'].unique()))

    with col3:
        selection3 = st.multiselect('Select Year', ['Select All'] + list(df['year'].unique()))
        
   
    
    if st.button("Analyze"): 
        
        if selection1[0] == 'Select All':
            df2 = df.copy()
        else:
            df2 = df[df['county'].isin(selection1)]
            
        if selection2[0] == 'Select All':
            df3 = df2.copy()
        else:
            df3 = df2[df2['state'].isin(selection2)]
        
        if selection3[0] == 'Select All':
            df4 = df3.copy()
        else:
            df4 = df3[df3['year'].isin(selection3)]
        
        st.success(f'Historical dataset contains {df4.shape[0]} rows and {df4.shape[1]} columns.')
        
        selected_feature_description = features_description[features_description['feature_name'] == column_name]
        
        st.markdown(f"### About {column_name}")
        st.markdown(f"{selected_feature_description['feature_description'].values[0]}")
        st.markdown(f"### Theoritical relationship of {column_name} with drought")
        st.markdown(f"{selected_feature_description['drought_trend'].values[0]}")
        
        sns.histplot(data = df4, x = column_name, color = color_code, edgecolor = color_code)
        plt.xlabel(column_name, fontsize = 15)
        plt.ylabel('Density', fontsize = 15)
        st.set_option('deprecation.showPyplotGlobalUse', False)
     
        st.markdown(f"### Distribution of {column_name}")
        
        st.pyplot()
        
        feature = column_name
        df[feature + '_Bin'] = pd.qcut(df4[feature], q = 5, duplicates = 'drop')
        binning_df = df.groupby(feature + '_Bin')['score'].mean().reset_index().rename(columns = {'score': 'Average Drought Score'})
        binning_df = binning_df.reset_index()
        binning_df['index'] = binning_df['index'] + 1
        binning_df[feature + '_Bin'] = binning_df['index'].astype(str) + '. ' + binning_df[feature + '_Bin'].astype(str)
        pal = sns.color_palette("Reds", len(binning_df['index']))
        sns.barplot(data = binning_df, x = feature + '_Bin', y = 'Average Drought Score', palette = pal)
        plt.xticks(rotation = 45)
        plt.xlabel(column_name, fontsize = 15)
        plt.ylabel('Average Drought Severity Level', fontsize = 15)
        
        st.markdown(f"### Average Drought Severity Levels v/s {column_name}")
        st.pyplot()

        
if __name__=='__main__': 
    main()