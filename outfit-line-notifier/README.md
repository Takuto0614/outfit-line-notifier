# outfit-line-notifier

毎朝7時に今日の天気をもとにおすすめコーデをLINEに通知するアプリです。

## セットアップ手順

### 1. Ollama をインストール・起動

[https://ollama.com](https://ollama.com) からインストールして以下を実行します。

```bash
ollama serve
ollama pull qwen2.5
```

### 2. プロジェクトのセットアップ

#### Windows

```bash
cd outfit-line-notifier
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Mac / Linux

```bash
cd outfit-line-notifier
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. config.py を編集

`config.py` を開いて以下を設定してください。

| クラス | 設定項目 | 説明 |
|---|---|---|
| `UserConfig` | NAME, GENDER, AGE, HEIGHT_CM | 個人情報 |
| `UserConfig` | STYLE_PREFERENCE, NG_ITEMS, FAVORITE_COLORS | ファッション好み |
| `LocationConfig` | LOCATION_NAME, LATITUDE, LONGITUDE | 住んでいる場所 |
| `LineConfig` | CHANNEL_ACCESS_TOKEN | LINE チャネルアクセストークン |
| `LineConfig` | USER_ID | LINE 通知先ユーザーID |
| `AppConfig` | NOTIFY_HOUR, NOTIFY_MINUTE | 通知時刻（デフォルト: 7:00） |
| `AppConfig` | OLLAMA_MODEL | 使用するOllamaモデル |

### LINE の設定方法

1. [LINE Developers](https://developers.line.biz/) でチャネルを作成
2. Messaging API チャネルのアクセストークンを `LineConfig.CHANNEL_ACCESS_TOKEN` に設定
3. 通知先ユーザーIDを `LineConfig.USER_ID` に設定（LINE公式アカウントマネージャーやWebhookで確認）

### 4. アプリ起動

#### 通常起動（毎朝7時に自動通知）

```bash
python main.py
```

Flaskサーバーが `http://127.0.0.1:5000` で起動します。

#### 即時実行（動作確認用）

```bash
python main.py --run-now
```

#### API経由で手動実行

```bash
curl -X POST http://127.0.0.1:5000/run-now
```

## ディレクトリ構成

```
outfit-line-notifier/
├── main.py                   # アプリ起動・Flaskサーバー
├── config.py                 # 各種設定定数
├── requirements.txt
├── README.md
├── services/
│   ├── weather_service.py    # 天気API (Open-Meteo)
│   ├── llm_service.py        # Ollama LLM呼び出し
│   ├── outfit_service.py     # プロンプト生成・コーデ提案
│   └── line_service.py       # LINE Messaging API
├── scheduler/
│   └── daily_scheduler.py    # APScheduler設定
└── utils/
    └── weather_code.py       # 天気コード→日本語変換
```

## モデル変更

`config.py` の `AppConfig.OLLAMA_MODEL` を変更するだけで切り替えられます。

```python
OLLAMA_MODEL = "llama3.1"   # または "mistral", "gemma" など
```

## エラー時の確認

| エラー | 確認事項 |
|---|---|
| 天気取得失敗 | インターネット接続を確認 |
| Ollama接続失敗 | `ollama serve` が起動しているか確認 |
| LINE通知失敗 | `CHANNEL_ACCESS_TOKEN` と `USER_ID` が正しいか確認 |
