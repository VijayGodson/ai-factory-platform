import os, time, logging
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI

app = FastAPI()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY", "mock-key-for-tests"),
    api_version="2024-06-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://mock-endpoint.openai.azure.com/"),
)

class NoteIn(BaseModel):
    text: str  # synthetic clinical note text only — never real PHI

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/summarize")
def summarize(note: NoteIn):
    start = time.time()
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize this synthetic clinical note in 2 sentences."},
            {"role": "user", "content": note.text},
        ],
        max_tokens=150,
    )
    latency_ms = int((time.time() - start) * 1000)
    usage = resp.usage
    logging.info({
        "event": "ai_call", "latency_ms": latency_ms,
        "prompt_tokens": usage.prompt_tokens, "completion_tokens": usage.completion_tokens,
    })
    return {"summary": resp.choices[0].message.content, "latency_ms": latency_ms}
