from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os, uuid

load_dotenv()

client = QdrantClient(os.getenv("QDRANT_URL"))
model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "meetings"

def create_collection_if_not_exists():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def embed_and_store(meeting_id: str, transcript: str, summary: str, action_items: list, decisions: list):
    create_collection_if_not_exists()

    chunks = []

    # chunk transcript into pieces
    words = transcript.split()
    chunk_size = 200
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append({"text": chunk, "type": "transcript"})

    # add summary as one chunk
    chunks.append({"text": summary, "type": "summary"})

    # add each action item as a chunk
    for item in action_items:
        chunks.append({"text": str(item), "type": "action_item"})

    # add each decision as a chunk
    for decision in decisions:
        chunks.append({"text": str(decision), "type": "decision"})

    points = []
    for chunk in chunks:
        vector = model.encode(chunk["text"]).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "meeting_id": meeting_id,
                "text": chunk["text"],
                "type": chunk["type"]
            }
        ))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Stored {len(points)} chunks for meeting {meeting_id}")