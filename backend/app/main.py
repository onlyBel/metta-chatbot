"""
Main entrypoint for running the FastAPI backend of MeTTA Chatbot.

You can run:
    uvicorn backend.main:app --reload
or use Docker with docker-compose.
"""

from .app import app

# If you want to run directly with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

