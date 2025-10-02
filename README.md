
## Weather Backend Service
A small backend service that fetches time-series weather data (temperature & humidity) from the Open-Meteo API and generates both an Excel file and a PDF report with charts.

## Prerequisites

Before running the project, ensure you have the following installed on your system:

Python 3.13

Pip (Python package manager)

SQLite (SQLite is included with Python standard library.)

Install Uv library .
## Features
Fetch weather data (temperature & humidity) for a given location (latitude & longitude) from Open-Meteo MeteoSwiss API.

Store the last 48 hours of weather data in a SQLite database.

#### REST API endpoints for:

/weather-report  -Fetch data from api and store data

/export/excel – Download last 48 hours of data as Excel (.xlsx)

/export/pdf – Generate a PDF report with charts for temperature & humidity

## Build with
Python 3.13

FastAPI

SQLite

Pandas (for Excel export)

Matplotlib / Plotly (for chart generation)

WeasyPrint (for PDF generation)

## API Endpoints

#### 1. Fetch Weather Data

```http
   GET api/weather-report
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Lattitude` | `float` | Lattitude|
| `Longitude` | `float` | Longitude|

lat – Latitude (e.g., 47.37)

lon – Longitude (e.g., 8.55)
#### Functionality:

Calls Open-Meteo API

Processes returned JSON

Stores timestamp, temperature, and humidity in SQLite DB

#### 2. Export Excel

```http
  GET api/export/excel
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Lattitude` | `float` | Lattitude|
| `Longitude` | `float` | Longitude|

#### Functionality:

Returns the last 48 hours of weather data in .xlsx format

Columns: timestamp | temperature_2m | relative_humidity_2m


#### 3. Export PDF Report


```http
 GET api/export/pdf
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Lattitude` | `float` | Lattitude|
| `Longitude` | `float` | Longitude|


#### Functionality:

Generates a PDF report containing:

Title & metadata (location, date range)

Line chart showing temperature & humidity vs time


## Running the Project
Using Python

python -m uv run uvicorn main:app --reload
