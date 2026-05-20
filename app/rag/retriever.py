from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"))
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "meetings"

def search_meetings(query: str, top_k: int = 5) -> list:
    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    ).points

    output = []
    for r in results:
        output.append({
            "text": r.payload["text"],
            "type": r.payload["type"],
            "meeting_id": r.payload["meeting_id"],
            "score": round(r.score, 3)
        })

    return output