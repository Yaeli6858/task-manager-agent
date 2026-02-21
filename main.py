from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware # הוספה
from agent_service import agent

app = FastAPI()

# מאפשר לאפליקציות חיצוניות (כמו ה-React שנבנה) לדבר עם השרת
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # מאפשר לכל מקור (כולל קבצים מקומיים) לגשת
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "השרת באוויר ומוכן לחיבור ה-UI!"}

@app.post("/chat")
def chat(msg: Message):
    return {"response": agent(msg.message)}