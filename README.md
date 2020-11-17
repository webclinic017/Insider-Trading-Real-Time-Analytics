# Insider-Trading-Real-Time-Analytics

Real-time automated ETL pipeline to visualize insider trading data. I use this project to store data scraped from [insider arbitrage](https://www.insidearbitrage.com/), visualize market activity for better decision making and analyze trends/patterns not readily observable, all in real-time.

## Techologies Used
* Selenium
* Apache Kakfka (PyKafka) 
* AWS Redshift
* Apache Airflow
* Tableau

## Overview

### Extract Live Data

- `Selenium` is used to scrape incoming data from multiple web sources, data is formatted into `JSON` where `kafka poducer` subsequently sends them to a `kafka topic`

<img src="https://github.com/AymenRumi/Insider-Trading-Real-Time-Analytics/blob/main/kafka.png" width="650" height="300">

### Transform & Load

 - `Kafka consumer` receives the data from the `kakfa topic`, transformed the data into relational format and queries it into an `AWS Redshift` data warehouse
 
 ### Live Tableau Dashboard

- `Tableau dashboard` is connected to `AWS Redshift`, the dashboard is updated real-time according to new entried added to Redshift

<img src="https://github.com/AymenRumi/Insider-Trading-Real-Time-Analytics/blob/main/dashboard.png" width="1000" height="550">

 ### Automation
 
 - `Apache Airflow` is used to call `bash scripts` that call and terminate `python scripts` at specific periods of time when the website posts incoming data
