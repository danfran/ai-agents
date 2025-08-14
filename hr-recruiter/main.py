from dotenv import load_dotenv

from vector_db import init_vector_store
from recruiting_agent import create_recruiter_agent
from graph import build_graph
import json


if __name__ == '__main__':
    load_dotenv()
    init_vector_store()

    agent = create_recruiter_agent()
    graph = build_graph()

    while True:
        prompt = input('Ask: ')

        if prompt == 'q':
            break

        response = graph.invoke({'messages': [('user', prompt)]})
        print('Assistant:\n')
        json_loads = json.loads(response['messages'][-1].content)
        print('-'*60)
        print(f"Name: {json_loads.get('name', 'Unknown')}\n")
        print(f"Candidate CV Summary: {json_loads.get('candidate_cv_summary', [])}\n")
        print(f"Matched skills: {', '.join(json_loads.get('matched_skills', []))}\n")
        print(f"Non matched skills: {', '.join(json_loads.get('non_matched_skills', []))}\n")
        print(f"Matched skills percentage: {json_loads.get('matched_skills_percentage', 0)}%")
        print('-' * 60)
