import requests


async def fetch_weather_data(lat: float, lon: float):
    print(f"Fetching weather data form api lat={lat}, lon={lon}")
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m"
        f"&past_days=2"   # get past 48 hours
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


#reprt=fetch_weather_data(lat=52.52, lon=13.405)  # Example call
#print(reprt)