from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.gemini import generate_recipe
from backend.models import RecipeRequest, RecipeResponse
from backend.safety import check_recipe


app = FastAPI(
    title="Cook AI",
    version="0.2.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Cook AI is running"
    }


@app.post("/api/recipe", response_model=RecipeResponse)
def create_recipe(request: RecipeRequest):

    recipe = generate_recipe(
        ingredients=request.ingredients,
        servings=request.servings,
    )

    safety = check_recipe(
        recipe=recipe,
        allergies=request.allergies,
    )

    return RecipeResponse(
        recipe=recipe,
        safety=safety,
    )
