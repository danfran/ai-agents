import json

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage

from model import State, InitialScreeningModelResponse
from tools import tools


MISSION_CONTROL_PROMPT = """
You are an HR recruiter for an IT company. Your task is to analyze candidate CVs to determine if they are a good match for the company's required skills.
The company requires expertise in: Glue, Spark, Python, Scala, and C#.

You have access to a tool named 'retrieve' to fetch a candidate's CV.

Instructions:
1. When the user asks about a candidate, use the 'retrieve' tool with the candidate's name to get their CV.
2. If the 'retrieve' tool indicates the CV is not in the store, inform the user and ask them to add it.
3. If the CV is successfully retrieved, analyze it and generate a JSON object containing the following keys:
   - 'name': The candidate's name.
   - 'candidate_cv_summary': A brief summary of the candidate's experience.
   - 'matched_skills': A list of skills from the CV that match the required company skills.
   - 'non_matched_skills': A list of skills from the CV that do not match the required company skills.
   - 'matched_skills_percentage': A percentage score of the matched skills out of the total required company skills.
4. Your final output MUST be a valid JSON object only. Do not include any other text or explanation.

This is an example of expected JSON object:
{{
    "name": "John Smith",
    "candidate_cv_summary": "John Smith is a Data Engineer with certification in Apache Spark 3.0 (Python). His experience includes working with AWS Managed Airflow, Athena.",
    "matched_skills": ["C#", "Python", "Scala"],
    "non_matched_skills": ["Spark", "Glue"],
    "matched_skills_percentage": 60
}}
"""

agent_executor = None

def parse_and_validate_output(output_string):
    try:
        data = output_string['output']
        json_string = data.strip('```json\n').strip('```').strip()
        parsed_json_output = json.loads(json_string)
        return InitialScreeningModelResponse(**parsed_json_output)
    except (json.JSONDecodeError, ValueError) as e:
        # Fallback for when the LLM doesn't produce valid JSON
        print(f"Error parsing output: {e}")
        return InitialScreeningModelResponse(
            name="Unknown",
            candidate_cv_summary="Could not parse agent's final response.",
            matched_skills=[],
            non_matched_skills=[],
            matched_skills_percentage=0
        )


def create_recruiter_agent(prompt=MISSION_CONTROL_PROMPT):
    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai", temperature=0)
    agent = create_tool_calling_agent(llm, tools, chat_prompt)
    global agent_executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False) | parse_and_validate_output


def recruiter_control(state: State):
    """Extracts intent from user input using a structured prompt and returns parsed JSON as an AIMessage. """
    user_input_content = state['messages'][-1].content
    output = agent_executor.invoke({'input': user_input_content})
    print(type(output))
    return {'messages' : [AIMessage(content=json.dumps(output))]}