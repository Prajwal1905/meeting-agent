from fastapi import APIRouter
from pydantic import BaseModel
from app.db.mongo import meetings_collection
from app.rag.retriever import search_meetings

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

@router.get("/meetings")
def get_all_meetings():
    meetings = list(meetings_collection.find({}, {"_id": 0}))
    return {"meetings": meetings}

@router.post("/search")
def search(request: SearchRequest):
    results = search_meetings(request.query)
    return {"results": results}