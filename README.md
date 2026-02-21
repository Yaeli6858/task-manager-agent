# Task Manager Agent 🤖

A simple AI-powered task manager that allows users to manage their daily tasks via natural language chat.

## Features

- Add, update, delete, and list tasks.
- Interact with tasks using natural language queries.
- Powered by a custom AI agent.
- FastAPI backend and optional React frontend for chat interface.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Yaeli6858/task-manager-agent.git

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate
venv\Scripts\activate     

Install dependencies:

pip install -r requirements.txt
Usage

Run the FastAPI server:

uvicorn main:app --reload

Open Postman or the React frontend to interact with the AI task manager.

Project Structure

todo_service.py – Core task management logic.

agent_service.py – AI agent logic for parsing user queries and executing tasks.

main.py – FastAPI server endpoints.

index.html / React frontend – Optional chat interface.