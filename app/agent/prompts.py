SUMMARY_PROMPT = """
You are an expert meeting analyst.
Read the following meeting transcript and provide a clear, concise summary in 8-10 bullet points.
Focus on the main topics discussed, key points raised, and overall context.

Transcript:
{transcript}

Return only the bullet points, nothing else.
"""

ACTION_ITEMS_PROMPT = """
You are an expert at extracting action items from meeting transcripts.
Read the transcript carefully and extract EVERY task or commitment made by any person.

Return ONLY a valid JSON array, no explanation, no markdown, no backticks:
[
  {{"person": "Name", "task": "what they need to do", "deadline": "deadline or Not specified"}}
]

Transcript:
{transcript}

Return only valid JSON array, nothing else.
"""

DECISIONS_PROMPT = """
You are an expert at extracting decisions from meeting transcripts.
Read the transcript and extract every decision that was made.

Return a JSON array like this:
[
  {{"decision": "what was decided", "made_by": "who decided or Group"}},
]

Transcript:
{transcript}

Return only valid JSON array, nothing else.
"""

EMAIL_PROMPT = """
You are a professional email writer.
Write a clear follow-up email based on this meeting information.

Summary:
{summary}

Action Items:
{action_items}

Decisions:
{decisions}

Write a professional, concise follow-up email with subject line.
Format: 
Subject: ...
Body: ...
"""