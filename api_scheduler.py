from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from cathay.cathaybk import crawler_cathaybk
from esun.esun_crawler import crawler_esun
import time


def crawler():
    crawler_cathaybk()
    crawler_esun()

scheduler = BackgroundScheduler(timezone='Asia/Taipei')
scheduler.add_job(
    crawler,
    trigger = 'cron',
    hour = 15,
    minute = 30,
    day_of_week = '*',      
    )


logger.info('sent_crawler_task')
scheduler.start()

while True:
    time.sleep(6000)

