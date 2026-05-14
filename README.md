# Project Genesis

This repository contains a production-quality FastAPI AI text analysis API.

## Features
- POST `/analyze`: AI-powered text analysis (summary, sentiment, intent).
- GET `/test`: Built-in test suite runner.
- Mock LLM mode for local development.

## Quick Start
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```