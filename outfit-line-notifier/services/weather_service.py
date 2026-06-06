import logging
from datetime import datetime

import requests

from config import LocationConfig
from utils.weather_code import to_japanese

logger = logging.getLogger(__name__)

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather() -> dict | None:
    """Open-Meteo APIから天気情報を取得して返す。失敗時はNoneを返す。"""
    params = {
        "latitude": LocationConfig.LATITUDE,
        "longitude": LocationConfig.LONGITUDE,
        "timezone": LocationConfig.TIMEZONE,
        "daily": [
            "weathercode",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
        ],
        "current_weather": True,
        "hourly": ["relativehumidity_2m"],
        "forecast_days": 1,
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logger.error("天気API取得失敗: %s", e)
        return None

    try:
        today = datetime.now().strftime("%Y-%m-%d")

        current = data["current_weather"]
        daily = data["daily"]
        hourly = data["hourly"]

        # 現在時刻に最も近い時間帯の湿度を取得
        current_hour = datetime.now().hour
        humidity = hourly["relativehumidity_2m"][current_hour]

        weather_code = daily["weathercode"][0]

        return {
            "location": LocationConfig.LOCATION_NAME,
            "date": today,
            "weather": to_japanese(weather_code),
            "current_temperature": round(current["temperature"]),
            "min_temperature": round(daily["temperature_2m_min"][0]),
            "max_temperature": round(daily["temperature_2m_max"][0]),
            "humidity": humidity,
            "precipitation_probability": daily["precipitation_probability_max"][0],
        }
    except (KeyError, IndexError, TypeError) as e:
        logger.error("天気データの解析に失敗しました: %s", e)
        return None
