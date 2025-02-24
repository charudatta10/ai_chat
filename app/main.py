from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import logging
import pathlib
import os

Home = pathlib.Path(__name__).parent / "app"  # Get the path to the app directory

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler(Home.parent / "app.log"),  # Log to a file
        logging.StreamHandler(),  # Log to the console
    ],
)

logger = logging.getLogger(__name__)  # Create a logger instance

app = FastAPI()

# Mount static files (for CSS, JS, etc.)
app.mount("/static", StaticFiles(directory=Home/"static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=Home/"templates")


# Homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    logger.info("Rendering homepage")  # Log the homepage request
    return templates.TemplateResponse({"request": request}, "index.html")


# Chat endpoint (accepts JSON)
@app.post("/chat")
async def chat(message: dict = Body(...)):
    logger.info("Received a new chat request")  # Log the start of the request
    user_input = message.get("message")
    if not user_input:
        logger.warning("No message provided in the request")  # Log a warning
        return JSONResponse({"error": "Message is required"}, status_code=400)

    logger.info(f"User input: {user_input}")  # Log the user input

    try:
        # Call the Ollama API
        logger.info("Calling Ollama API...")  # Log the API call
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen2.5:0.5b",
                "messages": [{"role": "user", "content": user_input}],
                "stream": False,
            },
        )
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Log the full API response
        logger.info(f"Ollama API response: {response.text}")

        # Extract the AI response
        ai_response = response.json().get(
            "message", "AI: Sorry, I couldn't process that."
        )
        logger.info(f"AI response: {ai_response}")  # Log the AI response
        return {"message": ai_response}
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama API request failed: {e}")  # Log the error
        return JSONResponse({"error": "Failed to process the request"}, status_code=500)
