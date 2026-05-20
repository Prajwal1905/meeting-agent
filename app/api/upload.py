from fastapi import APIRouter, UploadFile, File, HTTPException
from app.transcription.whisper import transcribe_audio
from app.db.mongo import meetings_collection
from app.agent.graph import run_agent
from app.rag.embedder import embed_and_store
from app.automation.n8n_client import trigger_n8n, send_slack_notification
import shutil, os, uuid
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_meeting(file: UploadFile = File(...)):
    try:
        meeting_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{meeting_id}_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File saved: {file_path}")

        print("Transcribing audio...")
        transcript = transcribe_audio(file_path)
        print("Transcription done.")

        print("Running LangGraph agent...")
        result = run_agent(transcript)
        print("Agent done.")

        meeting_doc = {
            "meeting_id": meeting_id,
            "filename": file.filename,
            "transcript": transcript,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "decisions": result["decisions"],
            "email_draft": result["email_draft"],
            "created_at": datetime.utcnow()
        }
        meetings_collection.insert_one(meeting_doc)
        print("Saved to MongoDB.")

        print("Embedding and storing in Qdrant...")
        embed_and_store(
            meeting_id=meeting_id,
            transcript=transcript,
            summary=result["summary"],
            action_items=result["action_items"],
            decisions=result["decisions"]
        )
        print("Qdrant done.")

        print("Triggering n8n automation...")
        await trigger_n8n({
            "meeting_id": meeting_id,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "decisions": result["decisions"],
            "email_draft": result["email_draft"]
        })

        print("Sending Slack notification...")
        await send_slack_notification({
            "summary": result["summary"],
            "action_items": result["action_items"]
        })
        print("Slack notified.")

        os.remove(file_path)

        return {
            "meeting_id": meeting_id,
            "transcript": transcript,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "decisions": result["decisions"],
            "email_draft": result["email_draft"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TranscriptRequest(BaseModel):
    transcript: str

@router.post("/upload-transcript")
async def upload_transcript(request: TranscriptRequest):
    try:
        meeting_id = str(uuid.uuid4())

        print("Running LangGraph agent on transcript...")
        result = run_agent(request.transcript)

        meeting_doc = {
            "meeting_id": meeting_id,
            "filename": "manual_transcript",
            "transcript": request.transcript,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "decisions": result["decisions"],
            "email_draft": result["email_draft"],
            "created_at": datetime.utcnow()
        }

        meetings_collection.insert_one(meeting_doc)

        embed_and_store(
            meeting_id=meeting_id,
            transcript=request.transcript,
            summary=result["summary"],
            action_items=result["action_items"],
            decisions=result["decisions"]
        )

        await trigger_n8n({
            "meeting_id": meeting_id,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "decisions": result["decisions"],
            "email_draft": result["email_draft"]
        })

        print("Sending Slack notification...")
        await send_slack_notification({
            "summary": result["summary"],
            "action_items": result["action_items"]
        })
        print("Slack notified.")

        return {
            "meeting_id": meeting_id,
            "transcript": request.transcript,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "decisions": result["decisions"],
            "email_draft": result["email_draft"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))