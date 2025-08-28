from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend (Vite) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, allow all. tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    # For now, hardcode a simple response
    if "basil" in query.question.lower():
        return {"answer": "Basil is a fragrant herb used in cooking, especially in Italian dishes. 🌿"}
    return {"answer": f"Sorry, I don’t know about {query.question} yet."}

