import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title = "US Drought Dashboard",
    layout = "wide",
    initial_sidebar_state = "expanded")

st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)

path = 'https://storage.googleapis.com/cropsafe-drought-prediction-data-store/'

df_reshaped = pd.read_csv(path + 'data/drought_dataset_sample_streamlit.csv')

def month_to_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'
    
df_reshaped['season'] = df_reshaped['month'].apply(month_to_season)

st.title('US Drought Dashboard')

year_list = list(df_reshaped.year.unique())[::-1]
season_list = list(df_reshaped.season.unique())[::-1]

col1, col2 = st.columns(2)

with col1:
    selection1 = st.multiselect('Select a year', ['Select All'] + year_list)

with col2:
    selection2 = st.multiselect('Select a season', ['Select All'] + season_list)
    
print(df_reshaped.shape)


if st.button("Analyze"):
    
    if selection1[0] == 'Select All':
        df_selected = df_reshaped.copy()
    else:
        df_selected = df_reshaped[(df_reshaped['year'].isin(selection1))]
        
    if selection2[0] == 'Select All':
        df_selected2 = df_selected
    else:
        df_selected2 = df_selected[(df_selected['season'].isin(selection2))]
    
    df_final = df_selected2.groupby(['state'])['score'].mean().reset_index()
    df_final['score'] = np.round(df_final['score'], 2)
    df_final = df_final.sort_values(by = 'score', ascending = False)

    
    def make_choropleth(input_df, input_id, input_column):

        choropleth = px.choropleth(input_df, locations = input_id, color = input_column, locationmode = "USA-states",
                                color_continuous_scale = "sunsetdark",
                                range_color = (0, max(df_selected.score)),
                                scope = "usa",
                                labels = {'score':'score'}
                                )

        choropleth.update_layout(
            template = 'simple_white',
            plot_bgcolor = 'rgba(0, 0, 0, 0)',
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            margin = dict(l = 0, r = 0, t = 0, b = 0),
            height = 350
        )
        return choropleth


    col = st.columns((7, 4), gap = 'medium')


    with col[0]:
        st.markdown('#### Drought Severity Levels by States')
        choropleth = make_choropleth(df_final, 'state', 'score')
        st.plotly_chart(choropleth, use_container_width = True)


    with col[1]:
        st.markdown('#### Top States')

        st.dataframe(df_final,
                    column_order = ("state", "score"),
                    hide_index = True,
                    width = None,
                    column_config = {
                        "states_name": st.column_config.TextColumn(
                            "States",
                        ),
                        "score": st.column_config.ProgressColumn(
                            "Drought Score",
                            format = "%f",
                            min_value = 0,
                            max_value = max(df_final.score),
                        )}
                    )

    with st.expander('About the data', expanded=True):
        st.write('''
            - Data: [U.S. Drought Monitor](https://droughtmonitor.unl.edu/About/ContactUs.aspx), 
            [NASA POWER Project](https://droughtmonitor.unl.edu/About/ContactUs.aspx)
            ''')
