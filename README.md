# Insider-Trading-Real-Time-Analytics

Real-time ETL pipeline to visualize insider trading data. I use this project to store data scraped from [insider arbitrage](https://www.insidearbitrage.com/), visualize market activity for better decision making and analyze trends/patterns not readily observable, all in real-time.

## Techologies Used
* Selenium
* Apache Kakfka (PyKafka) 
* AWS Redshift
* Apache Airflow

## Overview

### Extract Live Data

- `Selenium` is used to scrape data from multiple web sources and   `kafka poducer`  sends the data to a `kafka topic`
