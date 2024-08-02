from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
import os
from messages import (
    HEALTH_CHECK_MESSAGE,
    EMAILS_JSONL_NOT_FOUND,
    PROCESSING_EMAILS_ERROR,
    QUESTION_REQUIRED,
    PROCESS_EMAILS_FIRST,
    QUESTION_PROCESSING_ERROR,
    UNEXPECTED_RESPONSE_FORMAT,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

emails_jsonl_path = ''

@app.get("/")
async def health_check():
    return {"message": HEALTH_CHECK_MESSAGE}

@app.get("/process_emails")
async def process_emails():
    global emails_jsonl_path
    try:
        emails_jsonl_path = os.path.join(os.getcwd(), 'emails.jsonl')
        if not os.path.exists(emails_jsonl_path):
            raise HTTPException(status_code=400, detail=EMAILS_JSONL_NOT_FOUND)

        result = subprocess.run(['python', 'rag.py', 'process', emails_jsonl_path], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"{PROCESSING_EMAILS_ERROR}: {e.stderr}")

@app.get("/ask")
async def ask_question(q: str):
    global emails_jsonl_path
    if not q:
        raise HTTPException(status_code=400, detail=QUESTION_REQUIRED)
    if not emails_jsonl_path:
        raise HTTPException(status_code=400, detail=PROCESS_EMAILS_FIRST)

    try:
        result = subprocess.run(['python', 'rag.py', 'query', q, emails_jsonl_path], capture_output=True, text=True, check=True)
        response = json.loads(result.stdout)
        if 'answer' in response:
            return {"query": q, "answer": response['answer']}
        elif 'error' in response:
            raise HTTPException(status_code=500, detail=response['error'])
        else:
            raise HTTPException(status_code=500, detail=UNEXPECTED_RESPONSE_FORMAT)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"{QUESTION_PROCESSING_ERROR}: {e.stderr}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
