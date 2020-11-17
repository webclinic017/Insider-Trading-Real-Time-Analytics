"""
This script starts a Kafka producer that scrapes data from InsiderArbritrage every 15 minutes and pushed it to a topic 
Script scrapes for Insider Buying data
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pykafka import KafkaClient
import datetime
import time
import stockData
import os
import pandas as pd
import csv
import sys
import json


# Function to use to check entry in logfile
def entryExists(df,data_entry):

    for i in range(len(df)):

        if data_entry==list(df.iloc[i]):
            return True
    
    return False



# Initializing Kafka producer

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['testing']
producer = topic.get_sync_producer()


# Initializing selenium for webscraping

PATH="./chromedriver"
chrome_options = Options()  
chrome_options.add_argument("headless") 
driver = webdriver.Chrome(PATH,options=chrome_options,keep_alive=False)

while (datetime.datetime.now().hour)<22:

    url = "https://www.insidearbitrage.com/insider-buying/?desk=yes"
    driver.get(url) 
    # Log Dataframe
    try:
        df=pd.read_csv('log_buy.csv')
    except:
        df=None
        data_entry=[]

    entries_added=0

    # if the values start reappearing, stop execution
    for i in range(2,102):

        data=[]
        data_json = {}
        data_json['Transaction'] = 'Buy'

        # 
        tickerpath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[2]"""
        ticker = driver.find_element_by_xpath(tickerpath)
        data.append(ticker.text)
        data_json['Ticker']=ticker.text
       
        
        
        namepath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[3]"""
        name = driver.find_element_by_xpath(namepath)
        data.append(name.text)
        data_json['Trader Name']=name.text
        

        relationshippath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[4]"""
        relationship = driver.find_element_by_xpath(relationshippath)
        data.append(relationship.text)
        data_json['Relationship']=relationship.text


        datepath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[5]"""
        date = driver.find_element_by_xpath(datepath)
        data.append(date.text)
        data_json['Transaction Date']=date.text


        costpath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[6]"""
        cost = driver.find_element_by_xpath(costpath)
        data.append(cost.text)
        data_json['Cost']=cost.text

        sharespath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[7]"""
        shares = driver.find_element_by_xpath(sharespath)
        data.append(shares.text)
        data_json['# Shares']=shares.text

        valuespath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[8]"""
        totalvalue = driver.find_element_by_xpath(valuespath)
        data.append(totalvalue.text)
        data_json['Total Value']=totalvalue.text

        sharesheldpath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[9]"""
        sharesheld = driver.find_element_by_xpath(sharesheldpath)
        data.append(sharesheld.text)
        data_json['Shares Held']=sharesheld.text

        filingdatepath = f"""//*[@id="sortTableM"]/div[2]/table[2]/tbody/tr[{i}]/td[10]"""
        filingdate = driver.find_element_by_xpath(filingdatepath)
        data.append(filingdate.text)
        data_json['Filing Date']=filingdate.text
        
        if df is None:
            data_entry.append(data)
            # Push data to topic
            current_price,moving_average=(stockData.getStockPrice(ticker.text))
          
            data_json['Current Price']=current_price
  
            data_json['Moving Average']=moving_average
            message = json.dumps(data_json)
            producer.produce(message.encode('ascii'))
            entries_added=entries_added+1
        else:
            if entryExists(df,data):
                break
            else:
                print('False: {}'.format(data))
                with open('log_buy.csv','a') as fd:
                    wr = csv.writer(fd, dialect='excel')
                    wr.writerow(data)

                # Push data to topic
                current_price,moving_average=(stockData.getStockPrice(ticker.text))
          
                data_json['Current Price']=current_price
  
                data_json['Moving Average']=moving_average
                
                message = json.dumps(data_json)
                
                producer.produce(message.encode('ascii'))
                entries_added=entries_added+1


    if df is None:
        with open("log_buy.csv", "w",newline='') as f:   
            writer = csv.writer(f)
            writer.writerow(["Ticker", "Trader Name", "Relationship", "Transaction Date","Cost","# Shares","Total Value","Shares Held", "Filing Date"])
            writer.writerows(data_entry)


    print("Total Entries Added: {}".format(entries_added))

    time.sleep(60*15)

driver.close()
driver.quit()


os._exit(1)