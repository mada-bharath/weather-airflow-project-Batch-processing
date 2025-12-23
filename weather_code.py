from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import pandas as pd



def kelvin_to_celsius(temp_in_kelvin):
    return round(temp_in_kelvin - 273.15, 2)




def transform_load_data(ti):

    data = ti.xcom_pull(task_ids="extract_weather_data")

    transformed_data = {
        "City": data["name"],
        "Description": data["weather"][0]["description"],
        "Temperature_C": kelvin_to_celsius(data["main"]["temp"]),
        "Feels_Like_C": kelvin_to_celsius(data["main"]["feels_like"]),
        "Minimum_Temp_C": kelvin_to_celsius(data["main"]["temp_min"]),
        "Maximum_Temp_C": kelvin_to_celsius(data["main"]["temp_max"]),
        "Pressure": data["main"]["pressure"],
        "Humidity": data["main"]["humidity"],
        "Wind_Speed": data["wind"]["speed"],
        "Time_of_Record": datetime.utcfromtimestamp(data["dt"] + data["timezone"]),
        "Sunrise_Time": datetime.utcfromtimestamp(data["sys"]["sunrise"] + data["timezone"]),
        "Sunset_Time": datetime.utcfromtimestamp(data["sys"]["sunset"] + data["timezone"]),
    }

    df = pd.DataFrame([transformed_data])

    file_name = (
        "current_weather_data_hanamkonda_"
        + datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        + ".csv"
    )

    df.to_csv(
        f"s3://weather-101/{file_name}",
        index=False
    )

    print(f"Successfully uploaded {file_name} to S3 bucket weather-101")



default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 8),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}




with DAG(
    dag_id="weather_dag",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=["weather", "api", "s3"],
) as dag:

    is_weather_api_ready = HttpSensor(
        task_id="is_weather_api_ready",
        http_conn_id="weathermap_api",
        endpoint="/data/2.5/weather?q=Hanamkonda&APPID=<Your_API_ID>",
        poke_interval=30,
        timeout=300,
    )

    extract_weather_data = SimpleHttpOperator(
        task_id="extract_weather_data",
        http_conn_id="weathermap_api",
        endpoint="/data/2.5/weather?q=Hanamkonda&APPID=<Your_API_ID>",
        method="GET",
        response_filter=lambda r: json.loads(r.text),
        log_response=True,
    )

    transform_load_weather_data = PythonOperator(
        task_id="transform_load_weather_data",
        python_callable=transform_load_data,
    )

    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
