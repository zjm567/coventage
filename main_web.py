from covid19_risk_cal import risk_cal
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import folium 
from folium.plugins import StripePattern
import geopandas as gpd
import numpy as np

def main():

    # st.title("Conventage")
    st.markdown("<h1 style='text-align: center; color: White;'>Conventage</h1>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("Risk Calculator")
        age = st.number_input("Please Enter Your Age:", min_value = 0, max_value = 100, step = 1)
  
        mask = st.selectbox("Do you wear a mask? ",
                                options = ['Yes','No'])

        vaccination = st.selectbox("Are you vaccinated? ",
                                options = ['Yes','No'])

        geolocation = st.text_input("Please Enter Your State:", "The full US state name", max_chars =25)
        calculate_button = st.button("Calculate")
        if calculate_button:
            risk_value = risk_cal(age, mask, vaccination, geolocation)
            st.write("The overall risk is: ", risk_value,"%")

    with col_r:
        georisk_df = pd.read_csv("RiskCategoryforGeolocation.csv")

        # Import the GeoPanda shape file
        gdf = gpd.read_file('us_geo_shape.json')

        # Rename the column from NAME to State in gdf so we can merge two data frames
        gdf = gdf.rename(columns = {"NAME":"State"})
        # Merge our sample data (final_df and the geoJSON data frame on the key id.
        final_df = gdf.merge(georisk_df, on = "State")

        # Create the base map in Folium
        risk_map = folium.Map(location=[48, -102], zoom_start=4)

        # Set up Choropleth map
        folium.Choropleth(
        geo_data = final_df,
        data = final_df,
        columns = ['State',"Ratio"],
        key_on = "feature.properties.State",
        fill_color = 'YlGnBu',
        fill_opacity = 1,
        line_opacity = 0.2,
        legend_name = "COVID-19 Risk",
        smooth_factor = 0,
        Highlight = True,
        line_color = "#0000",
        name = "COVID-19 Risk",
        show = True,
        overlay = True,
        nan_fill_color = "White"
        ).add_to(risk_map)

        # Add the hover functionality.
        style_function = lambda x: {'fillColor': '#ffffff', 
                                    'color':'#000000', 
                                    'fillOpacity': 0.1, 
                                    'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 
                                        'color':'#000000', 
                                        'fillOpacity': 0.50, 
                                        'weight': 0.1}
        NIL = folium.features.GeoJson(
            data = final_df,
            style_function=style_function, 
            control=False,
            highlight_function=highlight_function, 
            tooltip=folium.features.GeoJsonTooltip(
                fields=['State','Ratio'],
                aliases=['State','COVID-19 Risk'],
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
            )
        )
        risk_map.add_child(NIL)
        risk_map.keep_in_front(NIL)
        folium_static(risk_map)
        st.write("Tips for Preventing!\n Here it is")
        st.write("- Wear a Mask")
        st.write("- Get a COVID-19 Vaccine")
        st.write("- Clean your hands often 20 seconds of handwashing or 60 percent alcohol hand sanitizer")
        st.write("- Cover your cough or sneeze with a tissue")
        st.write("- Clean frequently touched objects and surfaces daily")

if __name__ == '__main__':
    main()
