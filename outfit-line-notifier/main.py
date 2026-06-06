import argparse
import logging
import time

from flask import Flask, jsonify

from scheduler.daily_scheduler import start_scheduler
from services.line_service import build_message, send_line_message
from services.outfit_service import generate_outfit
from services.weather_service import get_weather

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def run_notify():
    """天気取得 → コーデ生成 → LINE通知 の一連の処理を実行する。"""
    logger.info("通知処理を開始します...")

    weather = get_weather()
    if weather is None:
        logger.error("天気情報の取得に失敗したため、通知をスキップします。")
        return

    logger.info("天気取得完了: %s", weather)

    business, casual = generate_outfit(weather)
    if business is None:
        logger.error("コーデ生成に失敗したため、通知をスキップします。")
        return

    message = build_message(weather, business, casual)
    logger.info("送信メッセージ:\n%s", message)

    send_line_message(message)
    logger.info("通知処理が完了しました。")


# 動作確認用API
@app.route("/run-now", methods=["POST"])
def api_run_now():
    run_notify()
    return jsonify({"status": "ok", "message": "通知処理を実行しました。"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="outfit-line-notifier")
    parser.add_argument(
        "--run-now",
        action="store_true",
        help="起動直後に1回通知処理を実行する",
    )
    args = parser.parse_args()

    if args.run_now:
        run_notify()
    else:
        # スケジューラーを起動してFlaskサーバーを立ち上げる
        start_scheduler(run_notify)
        logger.info("Flaskサーバーを起動します。手動実行: POST /run-now")
        try:
            app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
        except (KeyboardInterrupt, SystemExit):
            logger.info("アプリを終了します。")
