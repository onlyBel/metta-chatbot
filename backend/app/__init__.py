"""
Backend package for MeTTA Chatbot

This file marks the 'backend' directory as a Python package.
It also makes core objects importable at package level if needed.
"""

from .app import app  # re-export FastAPI app so "backend:app" works

