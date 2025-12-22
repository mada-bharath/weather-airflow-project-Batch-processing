👉 Automated Weather Data Pipeline using Apache Airflow & AWS

👉 Project Overview

This project implements a fully automated ETL pipeline that collects real-time weather data from the Open Weather API, processes it using Python, orchestrates tasks using Apache Airflow, and stores the cleaned data in Amazon S3 on a daily schedule.

The pipeline is deployed on an AWS EC2 instance, following production-like data engineering practices.

👉 Architecture:

Open Weather API → Python Transformations → Apache Airflow DAG
→ AWS EC2 → Amazon S3 (Daily Storage)


👉 Technologies Used:

Python – Data extraction & transformation

2. Apache Airflow – Workflow orchestration & scheduling

3. AWS EC2 – Pipeline execution environment

4. Amazon S3 – Cloud data storage

5. REST API – Open Weather data source

6. Linux – Server & environment management


👉 Pipeline Workflow:

Extract real-time weather data using OpenWeather API

2. Clean, normalize, and structure raw JSON data in Python

3. Orchestrate tasks using Airflow DAGs

4. Schedule pipeline to run daily

5. Store transformed data in Amazon S3

6. Ensure automation and fault tolerance

👉 Key Features:

Fully automated ETL pipeline

2. Cloud-deployed architecture

3. Scalable & modular design

4.Production-style orchestration

5.Daily scheduled execution

👉 Future Enhancements:

Load data into PostgreSQL / Redshift

2. Add data quality checks

3. Implement real-time streaming

Author:

MADA Bharath Reddy
Aspiring Data Engineer | AWS | Airflow | Python

