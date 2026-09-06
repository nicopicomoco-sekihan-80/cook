import json
import os

from dotenv import load_dotenv
from google import genai

from backend.models import Recipe


load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def generate_recipe(
    ingredients: list[str],
    servings: int,
) -> Recipe:

    prompt = f"""
あなたはCook AIのレシピ生成エンジンです。

あなたの目的は、料理初心者が画面を見ながら
一手ずつ料理できるレシピを生成することです。

以下の食材を使って、{servings}人分の料理を作ってください。

ユーザーが指定した食材:
{", ".join(ingredients)}

重要:
このレシピは一般的なレシピ文章ではありません。

CookのUIでは、
「今やることを1つだけ表示する」
という設計で使用します。

そのため、stepsには料理初心者が
1ステップずつ実行できる小さな作業単位を入れてください。

例えば、

悪い例:
「野菜を切って肉を炒めて調味料を加える」

良い例:
「キャベツを切る」
「玉ねぎを切る」
「豚肉を炒める」
「玉ねぎを加える」
「キャベツを加える」
「醤油を加える」

各Stepには以下を設定してください。

title:
画面に大きく表示する短いタイトル。

instruction:
初心者に話しかけるような簡単な説明。

action:
ユーザーが行う行動。
例:
"PREPARE"
"CUT"
"ADD"
"STIR"
"COOK"
"SEASON"
"PLATE"

amount_display:
初心者向けに表示する量。
例:
"200g"
"大さじ1"
"塩 2〜3振り"

分量が不要な場合はnull。

duration_seconds:
その工程のおおよその時間。
タイマーが不要な工程の場合はnull。

completion_condition:
初心者が「終わった」と判断できる具体的な条件。

悪い例:
「適切に炒める」

良い例:
「豚肉の赤い部分がなくなるまで炒める」

safety_message:
食品安全上の注意が必要な場合のみ設定してください。
不要ならnull。

特に肉・魚・卵などは、
安全な加熱が必要な工程を必ず含めてください。

食材名について:

ingredients[].nameには、
一般的で短い標準的な食材名を使用してください。

悪い例:
「豚肉（薄切りまたはこま切れ）」

良い例:
「豚肉」

食材名に括弧や複数候補を入れないでください。

また、ユーザーが指定していない食材を
必要以上に追加しないでください。

JSON以外の文章は絶対に返さないでください。

以下のJSON形式を厳守してください。

{{
  "title": "料理名",
  "servings": {servings},

  "ingredients": [
    {{
      "name": "標準的な食材名",
      "amount": "分量"
    }}
  ],

  "steps": [
    {{
      "step": 1,
      "title": "短いタイトル",
      "instruction": "初心者向けの説明",
      "action": "CUT",
      "amount_display": null,
      "duration_seconds": 120,
      "completion_condition": "切り終わったらOK",
      "safety_message": null
    }}
  ]
}}

Cookの設計思想:

- 一度に大量の作業を指示しない
- 1Step = 1つの主な行動
- 初心者が迷わない言葉を使う
- 「適量」「適宜」だけで済ませない
- 必要なら「小さじ」「大さじ」「g」「個」「振り」など、
  初心者が理解しやすい単位を使用する
- 料理の安全性を優先する
- 分からない安全条件を安全だと断定しない
"""



    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
        },
    )

    data = json.loads(response.text)

    return Recipe.model_validate(data)
