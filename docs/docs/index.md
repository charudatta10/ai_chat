# AI Chat Bot Documentation

This documentation provides an overview of the FastAPI application, its endpoints, and how to run it.

## Table of Contents

- [AI Chat Bot Documentation](#ai-chat-bot-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Directory Structure](#directory-structure)
  - [Installation](#installation)
  - [Local LLM Setup](#local-llm-setup)
  - [Logging Setup](#logging-setup)
  - [Endpoints](#endpoints)
    - [Homepage](#homepage)
    - [Chat Endpoint](#chat-endpoint)
  - [Running the Application](#running-the-application)

## Introduction

This FastAPI application demonstrates a simple web application with logging, static file serving, and template rendering. It includes endpoints for rendering a homepage and handling chat requests.

## Directory Structure

```sh
app/
├── __init__.py
├── main.py
├── static/
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
└── __pycache__/
    └── ...
.env
.gitattributes
.gitignore
app.log
archive.zip
LICENSE
README.md
requirements.txt
run.py
tasks.py
docs/
├── mkdocs.yml
└── docs/
    └── index.md
tests/
__pycache__/
    └── ...
```

## Installation

To install the required dependencies, run the following command:

```sh
pip install -r requirements.txt
```

## Local LLM Setup

>[!Important]
> An AI Chat application utilizing Ollama as its backend requires a running Ollama server instance. This server must be active and listening on port 11434 for the chatbot to function correctly. The application relies on this connection to access and utilize the language models provided by Ollama.

use following command to run ollama server

```pwsh
ollama serve
```

## Logging Setup

The application uses the `logging` module to set up logging to both a file and the console. The log configuration is defined as follows:

```python
import logging
import pathlib

Home = pathlib.Path(__name__).parent / "app"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(Home.parent / "app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
```

## Endpoints

### Homepage

- **URL**: `/`
- **Method**: `GET`
- **Response**: HTMLResponse
- **Description**: Renders the homepage using Jinja2 templates.

```python
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    logger.info("Rendering homepage")
    return templates.TemplateResponse("index.html", {"request": request})
```

### Chat Endpoint

- **URL**: `/chat`
- **Method**: `POST`
- **Request Body**: JSON
- **Response**: JSONResponse
- **Description**: Handles chat requests by calling the Ollama API and returning the AI response.

```python
@app.post("/chat")
async def chat(message: dict = Body(...)):
    logger.info("Received a new chat request")
    user_input = message.get("message")
    if not user_input:
        logger.warning("No message provided in the request")
        return JSONResponse({"error": "Message is required"}, status_code=400)

    logger.info(f"User input: {user_input}")

    try:
        logger.info("Calling Ollama API...")
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:0.5b",
                "messages": [{"role": "user", "content": user_input}],
                "stream": False,
            },
        )
        response.raise_for_status()
        logger.info(f"Ollama API response: {response.text}")

        ai_response = response.json().get("message", "AI: Sorry, I couldn't process that.")
        logger.info(f"AI response: {ai_response}")
        return {"message": ai_response}
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API request failed: {e}")
        return JSONResponse({"error": "Failed to process the request"}, status_code=500)
```

## Running the Application

To run the application, use the following command:

```sh
uvicorn app.main:app --port=8000
```

For further information or questions, please refer to the [FastAPI documentation](https://fastapi.tiangolo.com/).

Feel free to reach out if you need any more help or have questions!
