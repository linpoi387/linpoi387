# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 09:56:40 2024

@author: user_09
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from loguru import logger
import mysql.connector
# from apscheduler.schedulers.background import BackgroundScheduler

def crawler_esun():
    url = "https://www.esunbank.com/zh-tw/personal/deposit/rate/forex/foreign-exchange-rates/"
    web = requests.get(url)
    soup = BeautifulSoup(web.text, "html.parser")
    country_ori = soup.find_all('div', class_='col-auto px-3 col-lg-5 title-item')
    buy_ori = soup.find_all('div', class_='BBoardRate')
    sell_ori = soup.find_all('div', class_='SBoardRate')
    buy_cash_ori = soup.find_all('div', class_='CashBBoardRate')
    sell_cash_ori = soup.find_all('div', class_='CashSBoardRate')
    
    time.sleep(1)
    
    country = []
    for i in country_ori:
        it = i.text
        country.append(re.sub(r'\r\n\s+',"", it))
    
    
    buy = []
    for i in buy_ori:
        buy.append(i.text)
        
    sell = []    
    for i in sell_ori:
        sell.append(i.text)
    
    buy_cash = []
    for i in buy_cash_ori:
        buy_cash.append(i.text)
        if i == '':
            i.remove()
               
    sell_cash = []    
    for i in sell_cash_ori:
        sell_cash.append(i.text)
        if i == '':
            i.remove()   
                                     
    
    connection = mysql.connector.connect(
        host='localhost',
        database='crawler',
        user='root',
        password='test'
    )
    
    cursor = connection.cursor()
    
    sql = "INSERT INTO esun (country, buy, sell, buy_cash, sell_cash, timestamp) VALUES (%s, %s, %s, %s, %s, NOW())"
    
    for i in range(len(country)):
        values = (country[i], buy[i], sell[i], buy_cash[i], sell_cash[i] )
        cursor.execute(sql, values)
    
    connection.commit()
    logger.info("數據成功插入 MySQL")
          

if __name__ == '__main__':   
    crawler_esun()

# scheduler = BackgroundScheduler(timezone='Asia/Taipei')
# scheduler.add_job(
#     crawler_esun,
#     trigger = 'cron',
#     hour = 15,
#     minute = 5,
#     day_of_week = '*',      
#     )

# logger.info('sent_crawler_task')
# scheduler.start()

# while True:
#     time.sleep(6000)

