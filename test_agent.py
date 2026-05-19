from app.agent.graph import run_agent

sample_transcript = """
John: Alright everyone, let's get started. We need to discuss the product launch timeline.

Sarah: I think we should push the launch to March 15th. We need more time for testing.

John: Agreed. Let's make that the official date. Sarah can you send the updated timeline to the client by Friday?

Sarah: Yes I'll do that by Thursday actually.

Mike: I'll handle the marketing materials. I'll have the first draft ready by next Wednesday.

John: Perfect. Also we decided to go with the blue color scheme for the packaging, not the green one.

Sarah: Good call. Mike, make sure the marketing materials reflect that.

Mike: Got it. Blue it is.

John: One more thing — Raj, can you set up the testing environment by end of this week?

Raj: Sure, I'll have it ready by Friday.

John: Great. So to summarize — launch is March 15th, Sarah sends timeline Thursday, Mike has marketing draft Wednesday, Raj sets up testing by Friday. Any questions?

Everyone: No, sounds good.

John: Perfect, thanks everyone.
"""

result = run_agent(sample_transcript)

print("\n===== SUMMARY =====")
print(result["summary"])

print("\n===== ACTION ITEMS =====")
for item in result["action_items"]:
    print(item)

print("\n===== DECISIONS =====")
for d in result["decisions"]:
    print(d)

print("\n===== EMAIL DRAFT =====")
print(result["email_draft"])