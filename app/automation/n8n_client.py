import httpx
import os
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

async def trigger_n8n(meeting_data: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                N8N_WEBHOOK_URL,
                json=meeting_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            print(f"n8n triggered: {response.status_code}")
            return response.status_code
    except Exception as e:
        print(f"n8n trigger failed: {e}")
        return None

async def send_slack_notification(meeting_data: dict):
    try:
        summary = meeting_data.get("summary", "")
        action_items = meeting_data.get("action_items", [])
        
        action_text = "\n".join([
            f"• {item['person']}: {item['task']} (by {item['deadline']})"
            for item in action_items
        ])

        message = f"""🧠 *New Meeting Processed*

📋 *Summary:*
{summary}

✅ *Action Items:*
{action_text}"""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                SLACK_WEBHOOK_URL,
                json={"text": message},
                headers={"Content-Type": "application/json"},
                timeout=10.0
            )
            print(f"Slack notified: {response.status_code}")
    except Exception as e:
        print(f"Slack notification failed: {e}")