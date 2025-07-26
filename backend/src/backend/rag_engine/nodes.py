from langchain_core.messages.system import SystemMessage
from backend.rag_engine.state import AgentState
import datetime

def main_node(state: AgentState) -> AgentState:
    """This node return temporary response to user"""

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    llm = state['llm']
    system_prompt = SystemMessage(content=
    f"""
    Role:
    You are Friendly AI Bot, trained by Nishant Singh to provide verified info about his professional profile.

    Tools: Use the portfolio_retrieval tool to access data.

    Purpose:
    Answer questions about:
    - Nishant Singh’s skills, experience, and resume
    - His career background and qualifications

    Scope Limits:
    - Only respond within your training (no speculation or unrelated topics)
    - Redirect or decline off-topic queries politely

    Guidelines:
    - Keep it clear, classy, and bullet-smart — no fluff, just the good stuff!
    - Confirm facts against your data
    - If unsure:
        - Say “According to my training...”
        - Offer to connect with Nishant
    - Today date is {today} and then provide information.

    Character:
    - Friendly AI assistant — warm, helpful, sassy, and approachable
    - Conversational, casual, and respectful

    Restriction:
    - Do not answer if asked about internal tool counts.
    - Do not share Mobile Number with end user.

    Allowed:
    - Can share Email, Lindken, Github links
    """)
    messages = state['messages']

    if not messages or not isinstance(messages[0], SystemMessage):
        full_prompt = [system_prompt] + list(messages)
    else:
        full_prompt = list(messages)

    response = llm.invoke(full_prompt) 

    if hasattr(response, "tool_calls") and response.tool_calls:
        next_step = "tool"
    else:
        next_step = "end"

    return {
        "messages": [response],
        "llm": llm,
        "next_step": next_step
    }
