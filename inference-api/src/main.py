from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from model_loader import load_model
from recommender import recommend

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["model"] = load_model()  # loaded once at startup
    yield
    state.clear()


app = FastAPI(title="Movie Recommender", lifespan=lifespan)

# Lets the React frontend (on a different domain) call this API. Tighten later.
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"]
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/recommendations/{user_id}")
def get_recommendations(user_id: int, n: int = Query(10, ge=1, le=50)):
    try:
        recs = recommend(state["model"], user_id, n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"user_id": user_id, "recommendations": recs}