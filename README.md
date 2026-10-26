
# Remote Data Analysis Agent

## Overview

The Remote Data Analysis Agent is a Python-based AI agent that analyzes data and explains the results in simple English. It uses the Groq LLM and communicates with other agents through the Agent2Agent (A2A) protocol.

This agent works as a separate service. The AI Database Agent can send it analysis requests when more advanced analysis is needed.

## Project Objectives

- Analyze data received from another agent.
- Use a Groq language model to interpret the supplied data.
- Return understandable analysis and findings.
- Expose the agent through the A2A protocol.
- Allow other agents to communicate with it over HTTP.

## Architecture

1. The AI Database Agent sends a request to the Remote Data Analysis Agent.
2. The A2A server receives the request.
3. The agent processes the supplied data using Groq.
4. The analysis result is returned to the requesting agent.

## Technologies Used

- Python
- A2A SDK
- Groq API
- Uvicorn
- Python dotenv

## Project Files

- `a2a_server.py` — Starts the A2A server and exposes the agent.
- `remote_agent.py` — Contains the data-analysis logic.
- `test_a2a_client.py` — Used to test communication with the agent.
- `requirements.txt` — Lists the Python dependencies.
- `.env` — Stores configuration and API credentials. Do not commit this file.

## Prerequisites

- Python 3.13
- A Groq API key
- Internet access to reach the Groq API

## Installation

Clone or navigate to the project directory:

```bash
cd ~/Documents/razak_projects/remote_agent
```

Create and activate a virtual environment:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure your Groq API key in the `.env` file using the environment variable name expected by the application.

## Run the Agent

Start the server:

```bash
python a2a_server.py
```

The server is expected to listen on port `8001`.

Agent Card endpoint:

```text
http://localhost:8001/.well-known/agent-card.json
```

Open the Agent Card URL in a browser to inspect the agent's advertised information and capabilities.

## Integration with the AI Database Agent

The AI Database Agent can send analysis tasks to this agent through A2A. The remote agent analyzes the data it receives and returns its findings.

The remote agent does not directly query the PostgreSQL database in the intended architecture. The database agent retrieves the required information through MCP and passes the relevant results for analysis.

## Security Notes

- Keep `.env` and API keys private.
- Do not commit secrets to version control.
- Configure network access and authentication appropriately before exposing the service outside a trusted development environment.

## Current Scope

This project provides a remote AI data-analysis service using Groq and A2A. Further production features, such as authentication, monitoring, retries, and deployment configuration, can be added as needed.
