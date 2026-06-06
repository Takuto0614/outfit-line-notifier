import logging

import requests

from config import LineConfig, UserConfig

logger = logging.getLogger(__name__)

LINE_PUSH_URL = "https://api.line.me/v2/bot/message/push"


def build_message(weather: dict, business_outfit: str, casual_outfit: str) -> str:
    date_parts = weather["date"].split("-")
    date_str = f"{int(date_parts[1])}月{int(date_parts[2])}日"

    return (
        f"{UserConfig.NAME}さん、おはようございます！\n\n"
        f"今日の{weather['location']}の{date_str}の天気は{weather['weather']}、"
        f"気温は最低{weather['min_temperature']}℃ / 最高{weather['max_temperature']}℃、"
        f"湿度は{weather['humidity']}％です。\n\n"
        f"【ビジネスver】\n{business_outfit}\n\n"
        f"【休暇ver】\n{casual_outfit}\n\n"
        "今日も一日頑張りましょう！"
    )


def send_line_message(text: str) -> bool:
    """LINE Messaging APIでPushメッセージを送信する。成功時はTrue、失敗時はFalseを返す。"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LineConfig.CHANNEL_ACCESS_TOKEN}",
    }
    payload = {
        "to": LineConfig.USER_ID,
        "messages": [{"type": "text", "text": text}],
    }

    try:
        response = requests.post(LINE_PUSH_URL, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info("LINE通知を送信しました。")
            return True
        else:
            logger.error(
                "LINE通知失敗: status=%s, body=%s\n"
                "チャネルアクセストークンとユーザーIDが正しいか確認してください。",
                response.status_code,
                response.text,
            )
            return False
    except requests.RequestException as e:
        logger.error("LINE API呼び出し失敗: %s", e)
        return False
