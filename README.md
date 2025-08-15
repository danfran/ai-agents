# 🤖 My AI Agents Repository

Welcome to my collection of AI agent examples! This repository showcases various implementations of AI agents, each in its own dedicated directory.

Click on the links below to explore each agent's specific details, setup instructions, and code:

---

## Agent Examples

### [Agent Case 1: HR Recruiter CV Screener](hr-recruiter/README.md)
* **Description:** Simple agent that returns information about a candidate, based on the candidate's CV stored in a vector store (RAG).
* **Technologies:** Python, LangChain.

---

## Getting Started

To run any of these agents, navigate to its respective directory and follow the setup instructions in its `README.md` file.

**General Setup:**
1.  Clone this repository: `git clone https://github.com/danfran/ai-agents.git`
2.  Navigate to a specific agent's directory, for example: `cd ai-agents/hr-recruiter`
3.  Follow the instructions in the `README.md` located there.

---

## Build layer for AWS/Lambda

In this case for example, we are building a layer using Python 3.10

```bash
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.10" /bin/sh -c "pip install -r requirements.txt -t python/; exit"
```

Use the ECR gallery to find the image you are looking for: https://gallery.ecr.aws/sam/build-python3.10.

In alternative, use the Docker file included here if you are trying to create it using MacOS

```bash
docker build --tag 'ai_agent_aws_lambda_layer' .
# finally to copy the file locally
docker run -v ./lambda-layer-build:/usr/app/local --rm -it ai_agent_aws_lambda_layer sh -c "cp /usr/app/ai_agents_lambda_layer.zip /usr/app/local"
```
