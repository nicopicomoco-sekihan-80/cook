from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    amount: str


class RecipeStep(BaseModel):
    step: int
    title: str
    instruction: str
    action: str
    amount_display: str | None = None
    duration_seconds: int | None = None
    completion_condition: str
    safety_message: str | None = None


class Recipe(BaseModel):
    title: str
    servings: int
    ingredients: list[Ingredient]
    steps: list[RecipeStep]


class RecipeRequest(BaseModel):
    ingredients: list[str]
    servings: int = 2
    allergies: list[str] = Field(default_factory=list)


class SafetyIssue(BaseModel):
    type: str
    message: str
    ingredient: str | None = None


class SafetyResult(BaseModel):
    status: str
    issues: list[SafetyIssue] = Field(default_factory=list)
class RecipeResponse(BaseModel):
    recipe: Recipe
    safety: SafetyResult
