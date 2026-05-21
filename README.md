# MeetingMind — Agentic Meeting Intelligence System

> Upload a meeting recording. AI handles everything else.
> ## 🎥 Demo Video
[▶ Watch Live Demo](https://drive.google.com/drive/u/0/folders/1QGy19gVfNv8qH6autuTb5rFLNBdBx0W_)

---

MeetingMind is an end-to-end agentic AI system that automatically transcribes meeting audio, extracts action items and decisions, drafts follow-up emails, sends notifications, and enables semantic search across all past meetings.

---

## The Problem

Every company loses productivity to poorly followed-up meetings:
- Action items get forgotten
- Decisions are undocumented
- Next meeting repeats the same discussion
- Nobody knows what was decided 3 months ago

MeetingMind solves this completely automatically.

---

## How It Works
User uploads audio/transcript
        →
Whisper transcribes audio to text
        →
LangGraph Agent processes transcript
        →
Summary + Action Items + Decisions + Email Draft generated
        →
Stored in MongoDB + Qdrant (RAG)
        →
n8n triggered automatically
        →
Gmail email sent to attendees + Slack notification posted
        →
Search any past meeting anytime via RAG

---

## Features

- 🎙️ **Audio Transcription** — Upload any meeting recording, Whisper converts it to text
- 🤖 **Agentic Pipeline** — LangGraph multi-node agent extracts summary, action items, decisions
- 📧 **Auto Email** — Professional follow-up email sent automatically via n8n
- 💬 **Slack Notification** — Team channel notified instantly with meeting summary
- 🔍 **Semantic Search** — Search any past meeting by meaning, not just keywords
- 📝 **Transcript Paste** — Skip audio, paste Zoom/Meet transcript directly
- 🧠 **Cross-Meeting Intelligence** — Query across all meetings ever processed

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python |
| AI Agent | LangGraph, LangChain |
| LLM | Google Gemini 1.5 Flash |
| Transcription | OpenAI Whisper |
| Vector DB | Qdrant |
| Database | MongoDB |
| Automation | n8n |
| Notifications | Gmail, Slack |
| Frontend | React.js, Tailwind CSS |
| Deployment | Docker, Docker Compose |

---

---

## Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API Key (for Whisper)
- Google Gemini API Key (free)

### 1. Clone the repo

```bash
git clone https://github.com/Prajwal1905/meeting-agent.git
cd meeting-agent
```

### 2. Set up environment

```bash
cp  .env
```

Fill in your `.env`:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key
MONGODB_URL=mongodb://mongodb:27017
QDRANT_URL=http://qdrant:6333
N8N_WEBHOOK_URL=http://n8n:5678/webhook/meeting
SLACK_WEBHOOK_URL=your_slack_webhook
```

### 3. Start everything

```bash
docker-compose up --build
```

### 4. Access the app

- Frontend → `http://localhost:5173`
- Backend API → `http://localhost:8001`
- API Docs → `http://localhost:8001/docs`
- Qdrant Dashboard → `http://localhost:6333/dashboard`
- n8n Workflows → `http://localhost:5678`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload audio file |
| POST | `/api/upload-transcript` | Paste transcript text |
| POST | `/api/search` | Semantic search across meetings |
| GET | `/api/meetings` | Get all meetings |

---

---

## What Makes This Unique

Unlike Otter.ai or Fireflies.ai:

- **Fully agentic** — LangGraph reasoning, not rule-based extraction
- **Cross-meeting RAG** — semantic search across ALL past meetings
- **Multi-channel automation** — email + Slack in one pipeline
- **Self-hostable** — run everything locally with Docker
- **Open source** — fully customizable

---

## Built By

**Prajwal Khade**

[GitHub](https://github.com/Prajwal1905)
