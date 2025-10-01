from Core.DBCreation import DB

async def store_weather_data(data: dict,lattitude:float,longitude:float):
    try:
        _DB=DB()
        conn=_DB.DbConnection()
        cursor = conn.cursor()
        _DB.DbTableCreation()

        timestamps = data["hourly"]["time"]
        temps = data["hourly"]["temperature_2m"]
        hums = data["hourly"]["relative_humidity_2m"]
        #lattitude = data["latitude"]
        #longitude = data["longitude"]
        print(f"Storing weather data for lattitude={lattitude}, longitude={longitude}")
        # Convert lists to comma-separated strings
        ts_str = ",".join(timestamps)
        temp_str = ",".join(map(str, temps))   # convert each float to str
        hum_str = ",".join(map(str, hums)) 
        

        _data=await fetch_DBWeather_data(lattitude,longitude)
        if len(_data)>0:
            print(f"Data already exists for lattitude={lattitude}, longitude={longitude} and data={_data}   ")
            return True
        else:
            cursor.execute("""
                    INSERT INTO weather_info (lattitude,longitude,timestamp, temperature_2m, relative_humidity_2m)
                    VALUES (?, ?, ?,?,?)
                """, (lattitude,longitude,ts_str, temp_str, hum_str))
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"Error storing weather data: {e}")
        return False

async def fetch_DBWeather_data(lattitude:float,longitude:float):
    print(f"Fetching weather data from DB for lat={lattitude}, lon={longitude}")
    _DB=DB()
    conn=_DB.DbConnection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM weather_info where lattitude={lattitude} and longitude={longitude}")
    rows = cursor.fetchall()
    conn.close()
    return rows

#print(fetch_weather_data(52.52, 13.405))  # Example call