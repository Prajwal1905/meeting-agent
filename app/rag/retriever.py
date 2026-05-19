from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(os.getenv("QDRANT_URL"))
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "meetings"

def search_meetings(query: str, top_k: int = 5) -> list:
    query_vector = model.encode(query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )

    output = []
    for r in results:
        output.append({
            "text": r.payload["text"],
            "type": r.payload["type"],
            "meeting_id": r.payload["meeting_id"],
            "score": round(r.score, 3)
        })

    return output