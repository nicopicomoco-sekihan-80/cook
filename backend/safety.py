from backend.models import Recipe, SafetyIssue, SafetyResult


INGREDIENT_ALIASES = {
    "豚肉": [
        "豚肉",
        "豚薄切り肉",
        "豚バラ肉",
        "豚こま肉",
        "豚肩ロース",
        "豚ロース",
    ],
    "牛肉": [
        "牛肉",
        "牛薄切り肉",
        "牛バラ肉",
        "牛こま肉",
        "牛肩ロース",
        "牛ロース",
    ],
    "鶏肉": [
        "鶏肉",
        "鶏もも肉",
        "鶏むね肉",
        "鶏ささみ",
        "鶏ひき肉",
    ],
    "キャベツ": [
        "キャベツ",
    ],
    "玉ねぎ": [
        "玉ねぎ",
        "たまねぎ",
    ],
    "にんじん": [
        "にんじん",
        "人参",
    ],
    "じゃがいも": [
        "じゃがいも",
        "ジャガイモ",
        "馬鈴薯",
    ],
    "卵": [
        "卵",
        "たまご",
        "鶏卵",
    ],
    "牛乳": [
        "牛乳",
        "ミルク",
    ],
    "チーズ": [
        "チーズ",
    ],
    "小麦粉": [
        "小麦粉",
        "薄力粉",
        "強力粉",
    ],
    "醤油": [
        "醤油",
        "しょうゆ",
    ],
    "サラダ油": [
        "サラダ油",
        "植物油",
        "食用油",
        "キャノーラ油",
    ],
    "塩": [
        "塩",
        "食塩",
    ],
    "砂糖": [
        "砂糖",
        "上白糖",
    ],
}


def normalize_ingredient(name: str) -> str | None:
    for canonical_name, aliases in INGREDIENT_ALIASES.items():
        if name in aliases:
            return canonical_name

    return None


def check_recipe(
    recipe: Recipe,
    allergies: list[str],
) -> SafetyResult:

    issues: list[SafetyIssue] = []

    # --------------------------------
    # 1. 食材がSafety Engineに登録済みか
    # --------------------------------

    for ingredient in recipe.ingredients:

        canonical_name = normalize_ingredient(
            ingredient.name
        )

        if canonical_name is None:
            issues.append(
                SafetyIssue(
                    type="unknown_ingredient",
                    message=(
                        "この食材は現在のSafety Engineで"
                        "安全条件が確認されていません。"
                    ),
                    ingredient=ingredient.name,
                )
            )

    # --------------------------------
    # 2. アレルギー確認
    # --------------------------------

    for ingredient in recipe.ingredients:

        canonical_name = normalize_ingredient(
            ingredient.name
        )

        for allergy in allergies:

            if (
                allergy in ingredient.name
                or (
                    canonical_name is not None
                    and allergy == canonical_name
                )
            ):
                issues.append(
                    SafetyIssue(
                        type="allergy",
                        message=(
                            f"アレルギー指定「{allergy}」に"
                            "該当する可能性があります。"
                        ),
                        ingredient=ingredient.name,
                    )
                )

    # --------------------------------
    # 3. ステータス決定
    # --------------------------------

    if any(
        issue.type == "allergy"
        for issue in issues
    ):
        status = "BLOCKED"

    elif any(
        issue.type == "unknown_ingredient"
        for issue in issues
    ):
        status = "UNKNOWN"

    else:
        status = "SAFE"

    return SafetyResult(
        status=status,
        issues=issues,
    )
