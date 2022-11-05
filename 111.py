import pandas as pd
import geopandas as gpd
import leafmap
import ipyleaflet
import osmnx
import geocoder
import streamlit
from pyCIOT.data import *

epa_station = Air().get_data(src="OBS:EPA")
df_air = pd.json_normalize(epa_station) 
df_air['O3'] = 0
for index, row in df_air.iterrows():
  sensors = row['data']
  for sensor in sensors:
    if sensor['name'] == 'O3':
      df_air.at[index, 'O3'] =  sensor['values'][0]['value']
df_air = df_air[['name','location.latitude','location.longitude','O3']]

quake_station = Quake().get_station(src="EARTHQUAKE:CWB+NCREE")
df_quake = pd.json_normalize(quake_station) 
df_quake = df_quake[['name','location.latitude','location.longitude']]

gdf_air = gpd.GeoDataFrame(df_air, geometry=gpd.points_from_xy(df_air['location.longitude'], df_air['location.latitude']), crs='epsg:4326')
gdf_quake = gpd.GeoDataFrame(df_quake, geometry=gpd.points_from_xy(df_quake['location.longitude'], df_quake['location.latitude']), crs='epsg:4326')

m1 = leafmap.Map(center=(23.8, 121), toolbar_control=False, layers_control=True)
m1.add_gdf(gdf_air, layer_name="EPA Station")
m1.add_gdf(gdf_quake, layer_name="Quake Station")
m1