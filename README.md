# Insider-Trading-Real-Time-Analytics

Real-time ETL pipeline to visualize insider trading data. I use this project to store data scraped from [insider arbitrage](https://www.insidearbitrage.com/), visualize market activity for better decision making and analyze trends/patterns not readily observable, all in real-time.

## Techologies Used
* Selenium
* Apache Kakfka (PyKafka) 
* AWS Redshift
* Apache Airflow
* Tableau

## Overview

### Extract Live Data

- `Selenium` is used to scrape incoming data from multiple web sources, data is formatted into `JSON` where `kafka poducer` subsequently sends them to a `kafka topic`

<img src="https://github.com/AymenRumi/Insider-Trading-Real-Time-Analytics/blob/main/kafka.png" width="700" height="350">

### Transform & Load

 - `Kafka consumer` receives the data from the `kakfa topic`, transformed the data into relational format and queries it into an `AWS Redshift` data warehouse
 
 ### Tableau 

- `Tableau dashboard` is connected to `AWS Redshift`, the dashboard is updated real-time according to new entried added to Redshift
