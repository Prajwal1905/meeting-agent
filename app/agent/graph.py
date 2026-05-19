from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from app.agent.prompts import (
    SUMMARY_PROMPT,
    ACTION_ITEMS_PROMPT,
    DECISIONS_PROMPT,
    EMAIL_PROMPT
)
from typing import TypedDict
from dotenv import load_dotenv
import json, os

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-20250514",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

class AgentState(TypedDict):
    transcript: str
    summary: str
    action_items: list
    decisions: list
    email_draft: str

def summarize_node(state: AgentState) -> AgentState:
    prompt = SUMMARY_PROMPT.format(transcript=state["transcript"])
    response = llm.invoke([HumanMessage(content=prompt)])
    state["summary"] = response.content
    return state

def extract_actions_node(state: AgentState) -> AgentState:
    prompt = ACTION_ITEMS_PROMPT.format(transcript=state["transcript"])
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        state["action_items"] = json.loads(response.content)
    except:
        state["action_items"] = []
    return state

def extract_decisions_node(state: AgentState) -> AgentState:
    prompt = DECISIONS_PROMPT.format(transcript=state["transcript"])
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        state["decisions"] = json.loads(response.content)
    except:
        state["decisions"] = []
    return state

def draft_email_node(state: AgentState) -> AgentState:
    prompt = EMAIL_PROMPT.format(
        summary=state["summary"],
        action_items=json.dumps(state["action_items"]),
        decisions=json.dumps(state["decisions"])
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    state["email_draft"] = response.content
    return state

def run_agent(transcript: str) -> dict:
    graph = StateGraph(AgentState)

    graph.add_node("summarize", summarize_node)
    graph.add_node("extract_actions", extract_actions_node)
    graph.add_node("extract_decisions", extract_decisions_node)
    graph.add_node("draft_email", draft_email_node)

    graph.set_entry_point("summarize")
    graph.add_edge("summarize", "extract_actions")
    graph.add_edge("extract_actions", "extract_decisions")
    graph.add_edge("extract_decisions", "draft_email")
    graph.add_edge("draft_email", END)

    app = graph.compile()

    result = app.invoke({
        "transcript": transcript,
        "summary": "",
        "action_items": [],
        "decisions": [],
        "email_draft": ""
    })

    return result