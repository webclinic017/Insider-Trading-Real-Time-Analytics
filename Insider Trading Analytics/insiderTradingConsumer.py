from __future__ import division
"""
This script starts a Kafka consumer that moves data from the topic to an AWS Redshift database
Only new data entries will be added to Redshift
"""
# import libraries
import psycopg2
from pykafka import KafkaClient
import datetime
import time
import pandas as pd
import csv
import json
import math
import os
from itertools import islice
from pykafka.common import OffsetType


# create topic consumer

client = KafkaClient(hosts="localhost:9092")
topic = client.topics['testing']


# functions to send data to database


connection = psycopg2.connect(
    
    host="redshift-cluster-2.cr7enneqyugo.us-west-2.redshift.amazonaws.com",
    database="dev",
    port='5439',
    user="awsuser",
    password="621517Qwerty")

cursor=connection.cursor()



def sendToDB(json):

    (["Ticker", "Trader Name", "Relationship", "Transaction Date","Cost","# Shares","Total Value","Shares Held", "Filing Date"])

    ticker=json['Ticker']
    trader=json['Trader Name']
    relationship=json['Relationship']
    date=json['Transaction Date']
    transaction=json['Transaction']
    cost=float(json['Cost'].replace('$', ''))
    shares=int(json['# Shares'].replace(',', ''))
    total_value=int(json['Total Value'].replace(',', ''))
    sharesheld=int(json['Shares Held'].replace(',', ''))
    filing_date=json['Filing Date']
    current_price=float(json['Current Price'])
    moving_average=float(json['Current Price'])

    
    
    cursor.execute("Insert into InsiderTrading values('"+ticker+"','"+trader+"','"+relationship+"','"+date+"','"+transaction+"',"+str(cost)+","+str(shares)+","+str(total_value)+","+str(sharesheld)+",'"+filing_date+"',"+str(current_price)+","+str(moving_average)+");")
    connection.commit()

    
      

count=0
consumer = topic.get_simple_consumer(
        auto_offset_reset=OffsetType.LATEST,
        reset_offset_on_start=True)


LAST_N_MESSAGES = 5
# how many messages should we get from the end of each partition?
MAX_PARTITION_REWIND = int(math.ceil(LAST_N_MESSAGES / len(consumer._partitions)))
# find the beginning of the range we care about for each partition
offsets = [(p, op.last_offset_consumed - MAX_PARTITION_REWIND)
    for p, op in consumer._partitions.items()]
# if we want to rewind before the beginning of the partition, limit to beginning
offsets = [(p, (o if o > -1 else -2)) for p, o in offsets]

while (datetime.datetime.now().hour)<23:
    
    for message in islice(consumer, LAST_N_MESSAGES):
        count=count+1
        print(count)
        data=json.loads(message.value.decode())
        print(data)
        sendToDB(data)



os._exit(1)
        
        
        
        
        