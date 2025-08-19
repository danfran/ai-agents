import streamlit as st

from vector_db import init_vector_store
from recruiting_agent import create_recruiter_agent
from graph import build_graph


with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="file_qa_api_key", type="password")
    "[View the source code](https://github.com/danfran/ai-agents/blob/main/hr-recruiter/streamlit_app.py)"

st.title("🔎 HR assistant - Pre-screener for Candidates' CVs")
uploaded_file = st.file_uploader("Upload an article", type=("pdf"))
question = st.text_input(
    "Ask about matching skills for a candidate",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question and not gemini_api_key:
    st.info("Please add your Gemini API key to continue.")

if uploaded_file and question and gemini_api_key:
    init_vector_store(gemini_api_key)
    agent = create_recruiter_agent()
    graph = build_graph()

    response = graph.invoke({'messages': [('user', question)]})
    st.write("### Answer")
    st.write(response.completion)

    # json_loads = json.loads(response['messages'][-1].content)
    # print('-' * 60)
    # print(f"Name: {json_loads.get('name', 'Unknown')}\n")
    # print(f"Candidate CV Summary: {json_loads.get('candidate_cv_summary', [])}\n")
    # print(f"Matched skills: {', '.join(json_loads.get('matched_skills', []))}\n")
    # print(f"Non matched skills: {', '.join(json_loads.get('non_matched_skills', []))}\n")
    # print(f"Matched skills percentage: {json_loads.get('matched_skills_percentage', 0)}%")
    # print('-' * 60)