# Predicting-Illegal-Fishing-using-Machine-Learning

# Overview 
This project uses AIS data and spatial analysis to predict and flag potentially illegal fishing activity. A machine learning model is trained on vessel behavior to identify patterns indicative of fishing within Marine Protected Areas (MPAs).

# Features 

Accesses recent Global Fishing Watch data via API

Predicts fishing activity using a trained Random Forest model

Identifies illegal activity based on overlap with MPAs

Visualizes results on a map with vessel status color-coded

Built with GeoPandas, scikit-learn, matplotlib, PostGIS


# How it works 

Pull vessel event data via Global Fishing Watch API

Predict fishing activity with ML model

Filter vessel positions against ocean and MPA polygons

Visualize potential illegal activity on a map
