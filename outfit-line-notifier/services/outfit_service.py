import logging
import re

from config import UserConfig
from services.llm_service import call_ollama

logger = logging.getLogger(__name__)


def _build_prompt(weather: dict) -> str:
    ng_items = "、".join(UserConfig.NG_ITEMS)
    favorite_colors = "、".join(UserConfig.FAVORITE_COLORS)
    gender_label = "男性" if UserConfig.GENDER == "male" else "女性"

    return f"""あなたはファッションアドバイザーです。
以下のユーザー情報と天気情報をもとに、今日のおすすめコーデを日本語で提案してください。

# ユーザー情報
名前: {UserConfig.NAME}
性別: {gender_label}
年齢: {UserConfig.AGE}歳
身長: {UserConfig.HEIGHT_CM}cm
好みのスタイル: {UserConfig.STYLE_PREFERENCE}
避けたいアイテム: {ng_items}
好きな色: {favorite_colors}

# 天気情報
場所: {weather["location"]}
日付: {weather["date"]}
天気: {weather["weather"]}
現在気温: {weather["current_temperature"]}℃
最低気温: {weather["min_temperature"]}℃
最高気温: {weather["max_temperature"]}℃
湿度: {weather["humidity"]}%
降水確率: {weather["precipitation_probability"]}%

# 指示
以下の2パターンで服装を提案してください。回答は必ず下記フォーマットで出力し、余計な前置きや後書きは不要です。

【ビジネスver】
（ここにビジネス向けコーデの提案を1〜3文で書く）

【休暇ver】
（ここに休日向けコーデの提案を1〜3文で書く）

# 条件
- LINEで読みやすい文章にしてください
- 長すぎないようにしてください（各パターン1〜3文程度）
- 天気と気温に合った服装を提案してください
- 暑い日は通気性や汗対策に触れてください
- 寒い日は防寒に触れてください
- 雨の日は傘や防水靴に触れてください
- 湿度が高い日は蒸れにくい服装に触れてください
- 清潔感のある現実的な服装にしてください"""


def _parse_outfit(llm_response: str) -> tuple[str, str]:
    """LLMレスポンスからビジネスverと休暇verを抽出する。"""
    business = ""
    casual = ""

    business_match = re.search(
        r"【ビジネスver】\s*([\s\S]*?)(?=【休暇ver】|$)", llm_response
    )
    casual_match = re.search(r"【休暇ver】\s*([\s\S]*?)$", llm_response)

    if business_match:
        business = business_match.group(1).strip()
    if casual_match:
        casual = casual_match.group(1).strip()

    # パースに失敗した場合はレスポンス全体をビジネスverとして扱う
    if not business and not casual:
        business = llm_response.strip()
        casual = "（取得できませんでした）"

    return business, casual


def generate_outfit(weather: dict) -> tuple[str, str] | tuple[None, None]:
    """天気情報をもとにコーデ提案を生成する。(business, casual) のタプルを返す。"""
    prompt = _build_prompt(weather)
    logger.info("LLMにプロンプトを送信します...")

    response = call_ollama(prompt)
    if response is None:
        return None, None

    logger.info("LLMからレスポンスを受信しました。")
    return _parse_outfit(response)
