import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from typing import Literal
# from enum import Enum
# import instructor
load_dotenv() #reads .env and loads the key into environment

# class Priority (str, Enum):
#     HIGH = "High"
#     MEDIUM = "Medium"
#     LOW = "Low"

#-----PYDANTIC MODELS-----
class SubTask (BaseModel):
    title: str
    description: str

class MainTask(BaseModel):
    title: str
    SubTask: list[SubTask]
    priority: Literal["High", "Medium", "Low"]
    estimated_time: str #e.g. 3-4 hours

class TaskBreakdown(BaseModel):
    main_tasks : list[MainTask]
    final_chklist : list[str]


#-----CLIENT SETUP-----
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

#----CORE FUNCTION: TAKES A BRIEF, RETURNS STRUCTURED BREAKDOWN----
# brief = """
# Hey, I need a landing page for my product launch. It should have a hero section, pricing, and some testimonials. Can you also help with SEO stuff?
# """
def split_task(brief: str) -> TaskBreakdown:
    prompt = f"""You are project management assistant. A client has sent you the following rough project brief. Break it down into a clear, actionable plan.

CLIENT BRIEF:
{brief}

Please structure your response with these exact sections:
1. MAIN TASKS — the high-level chunks of the task
2. SUB-TASKS — under each main task, list the smaller steps that are needed
3. PRIORITY — mark each main task as High, Medium, or Low priority
4. ESTIMATED TIME — a rough time estimate for each main task
5. FINAL CHECHLIST — a flat, simple checklist covering everything, suitable for tracking the progress at a glance

Be concise but specific. If the brief is vague or missing details, make reasonable and useful assumptions and note them.
"""

    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt,
        config = GenerateContentConfig(
            response_mime_type = "application/json",
            response_schema = TaskBreakdown,
        ),
    )
    return response.parsed

#----UI----
st.title("AI Task Splitter")
st.write("Paste a rough client brief below and get a structured task breakdown.")

brief_input= st.text_area("Client brief ", height=150, placeholder="Paste the client's message here...")

if st.button("Split into Tasks"):
    if brief_input.strip()=="":
        st.warning("Please paste a brief first.")
    else:
        with st.spinner("Analysing brief.."):
            result = split_task(brief_input)
        st.session_state["result"] = result #save it to survive the reruns

#----Display the results----
if "result" in st.session_state:
    result = st.session_state["result"]

    st.header("Task Breakdown")

    priority_colours = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    for task in result.main_tasks:
        with st.expander(f"{priority_colours[task.priority]} {task.title} - {task.estimated_time}"):
            st.write(f"**Priority:** {task.priority}")
            st.write(f"**Sub_Tasks:**")
            for sub in task.SubTask:
                st.markdown(f"- **{sub.title}**: {sub.description}")

    st. header("Final Checklist")
    for i, item in enumerate(result.final_chklist):
        st.checkbox(item, key = f"check_{i}")