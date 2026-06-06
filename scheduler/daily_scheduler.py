import logging

from apscheduler.schedulers.background import BackgroundScheduler

from config import AppConfig

logger = logging.getLogger(__name__)


def start_scheduler(job_func) -> BackgroundScheduler:
    """毎朝指定時刻に job_func を実行するスケジューラーを起動して返す。"""
    scheduler = BackgroundScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(
        job_func,
        "cron",
        hour=AppConfig.NOTIFY_HOUR,
        minute=AppConfig.NOTIFY_MINUTE,
        id="daily_outfit_notify",
    )
    scheduler.start()
    logger.info(
        "スケジューラーを起動しました。毎朝 %02d:%02d に通知します。",
        AppConfig.NOTIFY_HOUR,
        AppConfig.NOTIFY_MINUTE,
    )
    return scheduler
