# Smart Guided Troubleshooter API

High-performance, context-aware diagnostic FastAPI service that processes natural language troubleshooting queries, retrieves relevant corrective procedures, and returns structured action steps, system categories, and deep links.

## Demo Video
> **Watch Demo:** [YouTube Video Link](https://youtu.be/n5QUuWbuMSo)

## Core Architecture & Features
- **FastAPI Pipeline:** `POST /troubleshoot` endpoint accepting `query` and `request_id`.
- **FastPath Cache & Retrieval:** Sub-millisecond context retrieval for device troubleshooting queries.
- **Action Validation:** Automated sequencing and deep link assignment for targeted device settings.

## Getting Started
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --reload
