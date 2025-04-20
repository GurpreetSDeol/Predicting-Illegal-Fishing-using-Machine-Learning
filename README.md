# Predicting-Illegal-Fishing-using-Machine-Learning

# Overview 
This project uses AIS data and spatial analysis to predict and flag potentially illegal fishing activity. A machine learning model is trained on vessel behavior to identify patterns indicative of fishing within Marine Protected Areas (MPAs).

# Features 

Accesses recent Global Fishing Watch data via API

Predicts fishing activity using a trained Random Forest model with a 97% accuracy. 

Identifies illegal activity based on overlap with MPAs

Visualizes results on a map with vessel status color-coded

Built with GeoPandas, scikit-learn, matplotlib, PostGIS


# How it works 

Pull vessel event data via Global Fishing Watch API

Predict fishing activity with ML model

Filter vessel positions against ocean and MPA polygons

Visualize potential illegal activity on a map

# Files
__Analysis.ipynb__: A visualisation of the MPZ's and fishing activity
__Filter_Fishing_data.ipynb__: Contains all of the data preprocessing steps
__Machine_Learning_Model.ipynb__: Development of the ML model
__Main.ipynb__: Contains functions for the API request, data filtering, ML prediction and plotting 
# Data Sources

Global Fishing Watch: Ship vessel data and API, including preprocessed labels indicating if a vessel is fishing.

Natural Earth Data: Ocean and Land boundaries.

Protected Planet: Marine Protected Zones (MPZ) boundaries.

Marine Conservation Institute: Marine Protected Zones (MPZ) boundaries.
