import pickle
import streamlit as st
import pandas as pd
import numpy as np

model=pickle.load(open('car_price_model.pkl','rb'))
car=pd.read_csv("Car_and_bike_final.csv")
images=pd.read_csv("Car_image.csv")


video_html = """
<style>
#myVideo {
  position: fixed;
  right: 0;
  bottom: 0;
  min-width: 100%;
  min-height: 100%;
}
</style>
<video autoplay muted loop id="myVideo">
  <source src="https://videos.pexels.com/video-files/6159292/6159292-sd_640_360_30fps.mp4"   
 type="video/mp4">
  Your browser does not support HTML5 video.
</video>
"""

st.markdown(video_html, unsafe_allow_html=True)
label_style = """
    <style>
    label {
        color: white !important;
        font-weight: bold !important;
        font-size: 20px !important;
    }
    </style>"""
st.markdown(label_style, unsafe_allow_html=True)


st.markdown("""
    <style>
    .title {
        color: white;
        text-align: center;
        font-size: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# Add the title with the custom CSS class
st.markdown('<h1 class="title">Car Valuation</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 7])

with col2:
    companies= sorted(car['Brand'].unique())
    option1 = st.selectbox('MAKER',companies,index=None,
        placeholder="Select the Manufacturer")

    name = car['Car Name'].loc[car['Brand'] == option1].unique()
    option2 = st.selectbox( 'MODEL', name,index=None,
        placeholder="Select the Model")

    # Get the image URL for the selected car name

    default_image_url = 'https://png.pngtree.com/png-vector/20190820/ourmid/pngtree-no-image-vector-illustration-isolated-png-image_1694547.jpg'
    image_url = images.loc[images['Title'] == option2, 'Image URL']

    if not image_url.empty:
        image_url = image_url.values[0]
    else:
        # Use a default image URL if the specific car image is not available
        image_url = default_image_url
    if option2:
        # Use custom CSS to set the image size
        st.markdown(
            f"""
        <style>
        .car-image-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin-top: 20px;
            color: white;
        }}
        .car-image {{
            width: 400px;
            height: 260px;
            object-fit: cover;
        }}
        .car-image-text {{  /* Add a new class for the image text */
        color: white;
        text-align: center;
        }}
        </style>
        <div class="car-image-container">
            <img src="{image_url}" alt="{option2}" class="car-image">
            <div class="car-image-text">{option2}</div>          
        </div>
        """,
            unsafe_allow_html=True
        )


with col1:
    Location= sorted(car['City'].unique())
    Place = st.selectbox( 'City', Location,index=None,
        placeholder="Popular Cities")

    Transmission= sorted(car['Transmission Type'].unique())
    custom_css = """
    <style>
    .st-radio label {
        color: white;  /* Set label text color to white */
    }
    </style>"""

    st.markdown(custom_css, unsafe_allow_html=True)
    transmission_type = st.radio(
        "TRANSMISSION",Transmission,horizontal=True,index=None)

    Fuel= sorted(car['Fuel Type'].unique())
    fuel_type=st.selectbox( 'FUEL', Fuel,index=None,
        placeholder="Fuel type")

    import datetime
    current_year = datetime.datetime.now().year
    years_list = list(range(current_year, 2004, -1))
    Year = st.selectbox( 'SELECT MANUFACTURING YEAR', years_list,index=None,
        placeholder="Select the Year")

    Km_driven= st.number_input(
        "KILOMETERS", min_value=0,max_value=125000 , placeholder="Enter Kilometer Driven")



if st.button('CHECK VALUE', type='primary'):
    if option2 and Km_driven and fuel_type and transmission_type and Place and Year:

        prediction = model.predict(pd.DataFrame([[option2, Km_driven, fuel_type, transmission_type, Place, Year]],
                                                columns=['Car Name', 'Kilometers Driven (in Km)', 'Fuel Type',
                                                         'Transmission Type', 'City', 'Year']))

        predict = str(np.round(prediction[0], 2))


        st.markdown(
             f"""
            <div style="font-size:28px; text-align:center;">
                Rs. <span style="font-size:48px; font-weight:bold; color:#FF6347;">{predict}</span> Lakh
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Please select all the options before checking the value.")
