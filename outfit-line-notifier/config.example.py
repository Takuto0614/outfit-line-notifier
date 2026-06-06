class UserConfig:
    NAME = "名前"
    GENDER = "male"       # "male" or "female"
    AGE = 25
    HEIGHT_CM = 170

    STYLE_PREFERENCE = "シンプル、清潔感"
    NG_ITEMS = ["派手すぎる服"]
    FAVORITE_COLORS = ["黒", "白", "グレー"]


class LocationConfig:
    LOCATION_NAME = "名古屋市栄"
    LATITUDE = 35.167
    LONGITUDE = 136.907
    TIMEZONE = "Asia/Tokyo"


class LineConfig:
    CHANNEL_ACCESS_TOKEN = "LINE Messaging API のチャネルアクセストークン（長期）"
    USER_ID = "通知先の LINE ユーザーID（U から始まる文字列）"


class AppConfig:
    NOTIFY_HOUR = 7
    NOTIFY_MINUTE = 0

    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "qwen2.5"   # llama3.1 / mistral / gemma なども可
