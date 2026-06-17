from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import students, predict, chat

app = FastAPI(title="EduLens API", version="1.0.0")

# Allow React dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(predict.router)
app.include_router(chat.router)

@app.get("/")
async def health():
    return {"status": "EduLens API is running"}