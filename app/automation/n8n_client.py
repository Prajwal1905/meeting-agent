import httpx
import os
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

async def trigger_n8n(meeting_data: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json=meeting_data,
                timeout=10.0
            )
            print(f"n8n triggered: {response.status_code}")
            return response.status_code
    except Exception as e:
        print(f"n8n trigger failed: {e}")
        return None