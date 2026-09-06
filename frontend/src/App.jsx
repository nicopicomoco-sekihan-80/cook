import { useState } from "react";
import "./App.css";

function App() {
  const [ingredients, setIngredients] = useState("");
  const [servings, setServings] = useState(2);
  const [loading, setLoading] = useState(false);
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState("");
  const [screen, setScreen] = useState("input");
  const [currentStep, setCurrentStep] = useState(0);

  const createRecipe = async () => {
    setLoading(true);
    setError("");
    setRecipe(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/recipe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ingredients: ingredients
            .split(/[,、\n]/)
            .map((item) => item.trim())
            .filter(Boolean),
          servings,
          allergies: [],
        }),
      });

      if (!response.ok) {
        throw new Error("レシピの生成に失敗しました");
      }

      const data = await response.json();

      setRecipe(data);
      setScreen("overview");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const startCooking = () => {
    setCurrentStep(0);
    setScreen("cooking");
  };

  const nextStep = () => {
    if (currentStep < recipe.recipe.steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setScreen("complete");
    }
  };

  const reset = () => {
    setRecipe(null);
    setScreen("input");
    setCurrentStep(0);
    setError("");
  };

  return (
    <div className="app">
      <main className="container">

        {/* =========================
            INPUT
        ========================= */}
        {screen === "input" && (
          <>
            <header className="hero">
              <div className="logo">🍳</div>
              <h1>Cook</h1>
              <p>料理を、ひとつずつ。</p>
            </header>

            <section className="card">
              <h2>何がある？</h2>

              <textarea
                value={ingredients}
                onChange={(e) => setIngredients(e.target.value)}
                placeholder="例：豚肉、キャベツ、玉ねぎ、醤油、塩、油"
                rows={4}
              />

              <div className="servings">
                <span>人数</span>

                <button
                  onClick={() =>
                    setServings(Math.max(1, servings - 1))
                  }
                >
                  −
                </button>

                <strong>{servings}人</strong>

                <button
                  onClick={() => setServings(servings + 1)}
                >
                  ＋
                </button>
              </div>

              <button
                className="start-button"
                onClick={createRecipe}
                disabled={loading || !ingredients.trim()}
              >
                {loading
                  ? "料理を考えています…"
                  : "🍳 作ってみる"}
              </button>

              {error && <p className="error">{error}</p>}
            </section>
          </>
        )}

        {/* =========================
            OVERVIEW
        ========================= */}
        {screen === "overview" && recipe && (
          <>
            <header className="hero small-hero">
              <div className="logo">🍳</div>
              <p>今日のCook</p>
            </header>

            <section className="card">
              <div className="recipe-header">
                <span>✨ レシピができました</span>

                <h2>{recipe.recipe.title}</h2>

                <p>
                  {recipe.recipe.servings}人分
                </p>
              </div>

              {/* Safety */}
              <div
                className={
                  recipe.safety.status === "SAFE"
                    ? "safety safe"
                    : "safety warning"
                }
              >
                {recipe.safety.status === "SAFE" ? (
                  <span>🟢 安全チェック：OK</span>
                ) : (
                  <>
                    <strong>⚠️ 安全チェック：確認が必要</strong>

                    {recipe.safety.issues?.map((issue, index) => (
                      <p key={index}>
                        {issue.ingredient
                          ? `${issue.ingredient}：`
                          : ""}
                        {issue.message}
                      </p>
                    ))}
                  </>
                )}
              </div>

              {/* Ingredients */}
              <div className="overview-section">
                <h3>🛒 材料</h3>

                <div className="ingredient-list">
                  {recipe.recipe.ingredients.map(
                    (ingredient, index) => (
                      <div
                        className="ingredient-row"
                        key={index}
                      >
                        <span>{ingredient.name}</span>
                        <strong>{ingredient.amount}</strong>
                      </div>
                    )
                  )}
                </div>
              </div>

              {/* Steps */}
              <div className="overview-section">
                <h3>🥘 作り方</h3>

                <div className="step-list">
                  {recipe.recipe.steps.map((step) => (
                    <div
                      className="overview-step"
                      key={step.step}
                    >
                      <div className="step-number">
                        {step.step}
                      </div>

                      <div>
                        <strong>{step.title}</strong>
                        <p>{step.instruction}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Time */}
              <div className="cook-time">
                ⏱ 全体の目安{" "}
                {Math.ceil(
                  recipe.recipe.steps.reduce(
                    (total, step) =>
                      total + (step.duration_seconds || 0),
                    0
                  ) / 60
                )}
                分
              </div>

              <button
                className="start-button"
                onClick={startCooking}
              >
                🍳 調理を始める
              </button>

              <button
                className="reset-button"
                onClick={reset}
              >
                別の料理を作る
              </button>
            </section>
          </>
        )}

        {/* =========================
            COOKING
        ========================= */}
        {screen === "cooking" && recipe && (
          <>
            <header className="cooking-header">
              <button
                className="back-button"
                onClick={() => setScreen("overview")}
              >
                ←
              </button>

              <span>
                {currentStep + 1} /{" "}
                {recipe.recipe.steps.length}
              </span>
            </header>

            <div className="progress">
              <div
                className="progress-bar"
                style={{
                  width: `${
                    ((currentStep + 1) /
                      recipe.recipe.steps.length) *
                    100
                  }%`,
                }}
              />
            </div>

            <section className="card cooking-card">
              <div className="step-label">
                STEP {currentStep + 1}
              </div>

              <h1>
                {recipe.recipe.steps[currentStep].title}
              </h1>

              <p className="instruction">
                {
                  recipe.recipe.steps[currentStep]
                    .instruction
                }
              </p>

              {recipe.recipe.steps[currentStep]
                .amount_display && (
                <div className="amount">
                  {
                    recipe.recipe.steps[currentStep]
                      .amount_display
                  }
                </div>
              )}

              {recipe.recipe.steps[currentStep]
                .completion_condition && (
                <div className="completion">
                  💡{" "}
                  {
                    recipe.recipe.steps[currentStep]
                      .completion_condition
                  }
                </div>
              )}

              {recipe.recipe.steps[currentStep]
                .safety_message && (
                <div className="step-safety">
                  ⚠️{" "}
                  {
                    recipe.recipe.steps[currentStep]
                      .safety_message
                  }
                </div>
              )}

              <button
                className="next-button"
                onClick={nextStep}
              >
                {currentStep ===
                recipe.recipe.steps.length - 1
                  ? "🎉 完成！"
                  : "できた！ ▶"}
              </button>
            </section>
          </>
        )}

        {/* =========================
            COMPLETE
        ========================= */}
        {screen === "complete" && recipe && (
          <section className="card complete-card">
            <div className="complete-icon">🎉</div>

            <h1>Cook Complete!</h1>

            <p>{recipe.recipe.title}</p>

            <div className="complete-message">
              おつかれさま！<br />
              料理が完成しました。
            </div>

            <button
              className="start-button"
              onClick={reset}
            >
              🍳 もう一度作る
            </button>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
