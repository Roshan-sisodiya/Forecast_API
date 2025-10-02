from fastapi import APIRouter, Depends
from DTO.Req_Res_DTO import ForecastRequestDTO, ForecastResponseDTO
from Services.ApiManager import fetch_weather_data
from Core.DBAction import store_weather_data, fetch_DBWeather_data 
import pandas as pd
from datetime import datetime, timedelta
from fastapi.responses import StreamingResponse,FileResponse
from io import BytesIO
from xlsxwriter import Workbook
import matplotlib.pyplot as plt
import tempfile, os
from weasyprint import HTML
import base64

router=APIRouter()

@router.get("/weather-report",response_model=ForecastResponseDTO)
async def get_weather_report(request: ForecastRequestDTO ):
    try:
        data=await fetch_DBWeather_data(request.Latitude, request.Longitude)
        #print(data)
        if len(data)==0:
            data = await fetch_weather_data(request.Latitude, request.Longitude)
        
            isstore= await store_weather_data(data,request.Latitude, request.Longitude)
            if isstore:
                return ForecastResponseDTO(
                    ReturnCode=200,
                    ReturnCodeDescription="Weather data fetched and stored successfully."
                )
            else:
                return ForecastResponseDTO(
                    ReturnCode=500,
                    ReturnCodeDescription="Weather data storing Failed."
                )
        else:
            return ForecastResponseDTO(
                ReturnCode=200,
                ReturnCodeDescription="Weather data already exists in DB."
            )
    except Exception as e:
        return ForecastResponseDTO(
            ReturnCode=500,
            ReturnCodeDescription=f"Weather data fetched and stored Failed with exception {e}."
        )

@router.get("/export/excel")
async def export_data(request: ForecastRequestDTO):
    try:
        data=await fetch_DBWeather_data(request.Latitude, request.Longitude)
        print(data)
        _data = []
        if len(data) == 0:
            info = await fetch_weather_data(request.Latitude, request.Longitude)
            await store_weather_data(info, request.Latitude, request.Longitude)
            data=await fetch_DBWeather_data(request.Latitude, request.Longitude)
            for row in data:
                temps = row[3].split(",")
                hums = row[4].split(",")
                timestamps = row[5].split(",")

                for t, temp, hum in zip(timestamps, temps, hums):
                    _data.append({
                    "timestamp": t,
                    "temperature_2m": float(temp),
                    "relative_humidity_2m": float(hum)
                })
        else:
            for row in data:
                temps = row[3].split(",")
                hums = row[4].split(",")
                timestamps = row[5].split(",")

                for t, temp, hum in zip(timestamps, temps, hums):
                    _data.append({
                    "timestamp": t,
                    "temperature_2m": float(temp),
                    "relative_humidity_2m": float(hum)
                })

        # Convert into DataFrame
        df = pd.DataFrame(_data)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Filter last 48 hours
        until = datetime.utcnow() + timedelta(hours=48)
        now = datetime.utcnow()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df[(df["timestamp"] >= now) & (df["timestamp"] <= until)]

        # Export to Excel in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Weather")
        output.seek(0)

        headers = {
            "Content-Disposition": 'attachment; filename="last_48_hours.xlsx"'
        }
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except Exception as e:
        return {"message": f"Failed to export data: {e}"}   

@router.get("/export/pdf")
async def export_data(request: ForecastRequestDTO):
    try:
        data=await fetch_DBWeather_data(request.Latitude, request.Longitude)
        #print(data)
        _data = []
        if len(data) == 0:
            info=await fetch_weather_data(request.Latitude, request.Longitude)
            await store_weather_data(info, request.Latitude, request.Longitude)
            data=await fetch_DBWeather_data(request.Latitude, request.Longitude)
            for row in data:
                temps = row[3].split(",")
                hums = row[4].split(",")
                timestamps = row[5].split(",")

                for t, temp, hum in zip(timestamps, temps, hums):
                    _data.append({
                    "timestamp": t,
                    "temperature_2m": float(temp),
                    "relative_humidity_2m": float(hum)
                })
        else:
            for row in data:
                temps = row[3].split(",")
                hums = row[4].split(",")
                timestamps = row[5].split(",")

                for t, temp, hum in zip(timestamps, temps, hums):
                    _data.append({
                    "timestamp": t,
                    "temperature_2m": float(temp),
                    "relative_humidity_2m": float(hum)
                })

        # Convert into DataFrame
        df = pd.DataFrame(_data)

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Filter last 48 hours
        until = datetime.utcnow() + timedelta(hours=48)
        now = datetime.utcnow()

        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df[(df["timestamp"] >= now) & (df["timestamp"] <= until)]

        if df.empty:
            return {"error": "No data available for last 48 hours"}

        # ---------------------------
        # 2. Generate chart with Matplotlib
        # ---------------------------
        plt.figure(figsize=(10, 5))
        plt.plot(df["timestamp"], df["temperature_2m"], label="Temperature (°C)", color="red")
        plt.plot(df["timestamp"], df["relative_humidity_2m"], label="Humidity (%)", color="blue")

        plt.xlabel("Time (UTC)")
        plt.ylabel("Values")
        plt.title("Weather Report - Last 48 Hours")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()

        # save chart to a temp file
        chart_path = os.path.join(tempfile.gettempdir(), "weather_chart.png")
        plt.savefig(chart_path)
        plt.close()

        # ---------------------------
        # 3. Build HTML for PDF
        # ---------------------------
        location = "Sample Location"  # replace with actual lat/lon if needed
        date_range = f"{now.strftime('%Y-%m-%d %H:%M')} → {until.strftime('%Y-%m-%d %H:%M')} UTC"
        with open(chart_path, "rb") as img_file:
            chart_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                h1 {{ text-align: center; }}
                .meta {{ text-align: center; margin-bottom: 20px; }}
                img {{ display: block; margin: auto; max-width: 100%; }}
            </style>
        </head>
        <body>
            <h1>Weather Report</h1>
            <div class="meta">
                <p><b>Location:</b> {location}</p>
                <p><b>Date Range:</b> {date_range}</p>
            </div>
            <img src="data:image/png;base64,{chart_base64}" />
        </body>
        </html>
        """

        # ---------------------------
        # 4. Render PDF
        # ---------------------------
        pdf_path = os.path.join(tempfile.gettempdir(), "weather_report.pdf")
        HTML(string=html_content).write_pdf(pdf_path)

        return FileResponse(pdf_path, filename="weather_report.pdf", media_type="application/pdf")
    except Exception as e:
        return {"message": f"Failed to export data: {e}"}