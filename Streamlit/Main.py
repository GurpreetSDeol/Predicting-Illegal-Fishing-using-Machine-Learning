import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import pickle
import gzip
import streamlit as st


class FishingAnalyser:

    def __init__(self):
        self.token = st.secrets["token"]

        base_path = os.path.dirname(__file__)
        
        model_path = os.path.join(base_path,  'random_forest_fishing_model.pkl.gz')
        
        with gzip.open(model_path, 'rb') as f:
            self.rf_model = pickle.load(f)
            
        with open('scaler.pkl', 'rb') as f:
              self.scaler = pickle.load(f)

        self.mpa_data = gpd.read_file(
            os.path.join(base_path, 'Data', 'Simple_mpz', 'simplified_zoneassessment_geom.shp')
        ).to_crs(epsg=4326)

        self.ocean_data = gpd.read_file(
            os.path.join(base_path, 'Data', 'ne_110m_ocean', 'ne_110m_ocean.shp')
        )

        self.land_data = gpd.read_file(
            os.path.join(base_path, 'Data', 'ne_10m_land', 'ne_10m_land.shp')
        )

    def api_request(self, start_date, end_date, limit):
        import requests
        url = 'https://gateway.api.globalfishingwatch.org/v3/events'
        if not (1 <= limit <= 100):
            print("Please enter a value between 1 and 100.")
            return

        params = {
            'datasets[0]': 'public-global-fishing-events:latest',
            'start-date': start_date,
            'end-date': end_date,
            'limit': limit,
            'offset': 0
        }

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            extracted_data = []

            for i in range(limit):
                lat = data['entries'][i]['position'].get('lat')
                lon = data['entries'][i]['position'].get('lon')
                distance_from_shore = data['entries'][i]['distances'].get('startDistanceFromShoreKm') * 1000
                distance_from_port = data['entries'][i]['distances'].get('startDistanceFromPortKm') * 1000
                speed = data['entries'][i]['fishing'].get('averageSpeedKnots')
                vessel_id = data['entries'][i]['vessel'].get('id')
                extracted_data.append([vessel_id, speed, distance_from_shore, distance_from_port, lat, lon])

            return pd.DataFrame(
                extracted_data,
                columns=['vessel_id', 'speed', 'distance_from_shore', 'distance_from_port', 'lat', 'lon']
            )
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            print(response.text)
            return None

    def filter_through_ocean(self, df):
        geometry = [Point(lon, lat) for lon, lat in zip(df['lon'], df['lat'])]
        ship_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        filtered_ships = gpd.sjoin(ship_gdf, self.ocean_data, how='inner', predicate='within')
        return filtered_ships[['vessel_id', 'speed', 'distance_from_shore', 'distance_from_port', 'lat', 'lon']]

    def predict_fishing_status(self, df):
        model_input = df.drop(['vessel_id'], axis=1).values
        model_input_scaled = self.scaler.transform(model_input)
        rf_predictions = self.rf_model.predict(model_input_scaled)
        df['prediction'] = rf_predictions
        df['status'] = df['prediction'].map({0: 'Not Fishing', 1: 'Fishing'})
        return df

    def filter_through_mpz(self, df):
        geometry = [Point(lon, lat) for lon, lat in zip(df['lon'], df['lat'])]
        ship_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

        intersections = gpd.sjoin(ship_gdf, self.mpa_data, how='inner', predicate='within')
        intersecting_indices = intersections.index.unique()

        def assign_illegal_status(row):
            if row.name in intersecting_indices:
                return 'yes' if row['prediction'] == 1 else 'maybe'
            return 'no'

        df['illegal'] = df.apply(assign_illegal_status, axis=1)
        geo_df = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
        return geo_df

    def plot(self, geo_df, point_size, return_fig=True):
        color_map = {'yes': 'red', 'maybe': 'orange', 'no': 'green'}
        geo_df['color'] = geo_df['illegal'].map(color_map)

        fig, ax = plt.subplots(figsize=(14, 10))
        self.land_data.plot(ax=ax, color='lightgray', edgecolor='white', linewidth=0.5)
        self.mpa_data.plot(ax=ax, color='deepskyblue', alpha=0.6, edgecolor='black', linewidth=0.3)

        for status, color in color_map.items():
            subset = geo_df[geo_df['illegal'] == status]
            if not subset.empty:
                subset.plot(ax=ax, markersize=point_size, color=color, label=status, alpha=0.8)

        ax.legend(title='Illegal Fishing')
        ax.set_title("Illegal Fishing Activity in MPAs", fontsize=16)
        ax.set_axis_off()
        plt.tight_layout()

        return fig if return_fig else None
