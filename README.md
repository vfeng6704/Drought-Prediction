## Executive Summary

The rising threat of climate change has significantly increased drought risks, affecting agricultural productivity and leading to financial losses. This project leverages advanced machine learning techniques to predict drought severity, providing valuable insights for crop insurance providers to enhance their products and support farmers.

### Problem Definition

Drought is a complex and gradual phenomenon that poses significant challenges for agricultural productivity. Accurate prediction of drought severity is crucial for insurance providers to mitigate risks and for farmers to make informed decisions. This project utilizes meteorological, soil, and topographical data to develop predictive models for drought severity, enabling better risk management and safer farming practices.

## Data Sources

- **NASA Power Project**: Weather data collected over the period of 2000-2016, aggregated daily.
- **FAO (Food and Agricultural Organization of the United Nations)**: Soil data with various topographical attributes.
- **Derived Features**: Meteorological and topographical attributes such as Humidex, Evapotranspiration, Slope, Soil Quality Index, etc.

## Methodology

- **Data Cleaning**:
  - Aggregated meteorological features using a 180-day rolling average.
  - Processed soil and topographical data for feature extraction.
  - Addressed multicollinearity and regional cyclicality.

- **Feature Engineering**:
  - Derived and selected features such as Relative Humidity, Cumulative Precipitation, Diurnal Temperature Range, and Soil Quality Index.
  - Reduced feature set to 16 predictors using methods like Recursive Feature Elimination and domain knowledge.

- **Modeling**:
  - **Model Selection**: Compared regression models like Random Forest Regressor, Decision Tree Regressor, and XGBoost Regressor.
  - **Performance Metrics**: RMSE was used to evaluate model accuracy.

## Lessons Learned

- **Feature Selection**: Domain knowledge and multicollinearity analysis were critical in reducing the feature set to the most predictive attributes.
- **Model Selection**: Random Forest Regressor provided the best performance, balancing interpretability with predictive accuracy.

## Future Work

- **Incorporate Additional Data Sources**: Explore the inclusion of crop-specific risk data, satellite imagery, and global trend data.
- **Improve Time-Series Modeling**: Enhance time-series techniques to better capture temporal dependencies and improve model performance.
- **Real-Time Implementation**: Integrate real-time data to provide timely insights for insurance providers and farmers.
