import streamlit as st
import plotly.express as px

import requests

API_KEY = "cf32f169c04a4026dc59da06763a4be5"



st.title("Weather forcast for the next days")

place =  st.text_input("Place", "Bucharest")
days = st.slider("Days",
                 min_value=1,
                 max_value=5,
                 help="Select the number of days for the forcast")
select = st.selectbox("Select Data View",
                      ("Temperature","Sky"))
st.subheader(f"{select} forcast for the {days} days in {place}")


def get_forecast(place, days):
    try:
        weather_url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"
    except KeyError:
        st.error("Please check the place name")
        return
    response = requests.get(weather_url)
    data = response.json()
    # print(data['list'][:days])
    return data['list'][:days * 8]

def get_data(place ,days, type="Temperature"):
    data = get_forecast(place, days)
    dates = [forcast['dt_txt'] for forcast in data]
    if type == "Temperature":
        temperatures = [int(forcast['main']['temp'])/10 for forcast in data]
        fig = px.line(x=dates, y=temperatures,
                      labels={"y": "Temperature", "x": "Days"})
        st.plotly_chart(fig)
    else :
        temperatures = [forcast['weather'][0]['main'] for forcast in data]

        cols = [1,2,3,4]
        for j in range(0, days ):
            cols[j] = st.columns(8)

        for i, temp in enumerate(temperatures):
            img_name = f"images/{temp.lower()}.png"
            cols[int(i/8)][i  % 8].image(img_name, width=100, caption=dates[i])

    return dates, temperatures

get_data(place,int(days), select)

# st.image("images/photo.png")

