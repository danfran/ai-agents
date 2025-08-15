# HR Recruiter

Simple agent that returns information about a candidate, based on the candidate's CV stored in a vector store (RAG).

It is a sort of CV pre-screener that will return a percentage of the matched skills and other candidate's info.

---

## Installation

First run the following commands:

```bash
cd hr-recruiter
python -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

then reate a file `.env` with the following content:

```bash
GOOGLE_API_KEY=<YOUR KEY TO USE GEMINI LLM>
BASE_DOCUMENTS=<YOUR PATH FOR PRE-ADDED CANDIDATE'S CVS>
```

and finally run the process with:

```bash
python main.py
```
---
