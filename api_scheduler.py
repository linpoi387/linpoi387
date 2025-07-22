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
    hour = 12,
    # minute = 5,
    day_of_week = '*',
    misfire_grace_time = 600  # 寬限時間為 600 秒      
    )

logger.info('sent_crawler_task')
scheduler.start()


time.sleep(1800)
   
    
