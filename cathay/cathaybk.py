# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 14:56:46 2024

@author: user_09
"""


import requests
from bs4 import BeautifulSoup
import time
import mysql.connector
from loguru import logger
# from apscheduler.schedulers.background import BackgroundScheduler

def crawler_cathaybk():
    url = "https://accessibility.cathaybk.com.tw/exchange-rate-search.aspx"
    web = requests.get(url)
    soup = BeautifulSoup(web.text, "html.parser")
    findAll = soup.find_all('td', class_='td')
    country_all = [findAll[i].text for i in range(len(findAll)) if i % 3 == 0]
    country = [country_all[i] for i in range(len(country_all)) if i != 19 and i != 14 and i != 5 and i != 3 and i != 1]
    
    buy_all = [findAll[i].text for i in range(len(findAll)) if i % 3 == 1]
    
    sell_all = [findAll[i].text for i in range(len(findAll)) if i % 3 == 2]
    
    keep_indices = [1, 3, 5, 14, 19]
    new_positions = [0, 1, 2, 10, 14]
    
    buy_cash = [""] * (max(new_positions) + 2)
    for original_index, new_index in zip(keep_indices, new_positions):
        buy_cash[new_index] = buy_all[original_index]

    
    sell_cash = [""] * (max(new_positions) + 2)
    for original_index, new_index in zip(keep_indices, new_positions):
        sell_cash[new_index] = sell_all[original_index]
    
    buy = [i for i in buy_all if i not in buy_cash]
    
    sell = [i for i in sell_all if i not in sell_cash]
    
    
    time.sleep(1)

    # print(country)
    # print(buy)
    # print(sell)
    # print(buy_cash)
    # print(sell_cash)
    
    connection = mysql.connector.connect(
        host='localhost',
        database='crawler',
        user='root',
        password='test'
    )
    
    cursor = connection.cursor()
    
    sql = "INSERT INTO cathaybk (country, buy, sell, buy_cash, sell_cash, timestamp) VALUES (%s, %s, %s, %s, %s, NOW())"
    
    for i in range(len(country)):
        values = (country[i], buy[i], sell[i], buy_cash[i], sell_cash[i] )
        cursor.execute(sql, values)
    
    connection.commit()
    logger.info("數據成功插入 MySQL")

if __name__ == '__main__':
    crawler_cathaybk()

# scheduler = BackgroundScheduler(timezone='Asia/Taipei')
# scheduler.add_job(
#     crawler_cathaybk,
#     trigger = 'cron',
#     hour = 15,
#     minute = 5,
#     day_of_week = '*',      
#     )

# logger.info('sent_crawler_task')
# scheduler.start()


# while True:
#     time.sleep(6000)


