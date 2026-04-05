from fastapi import FastAPI, HTTPException
from backend.models import QueryRequest, QueryResponse, SummarizeRequest
from backend.utils import ask_llm, get_system_prompt, get_summary_prompt, format_chat_history
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Offline AI Study Assistant Backend")

@app.get("/")
async def root():
    return {"message": "Welcome to the Offline AI Study Assistant API"}

@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Handles student queries with mode-based prompt engineering.
    """
    try:
        system_prompt = get_system_prompt(request.mode, request.language)
        messages = format_chat_history(request.history, system_prompt, request.query)
        
        answer = await ask_llm(messages)
        
        return QueryResponse(
            answer=answer,
            mode=request.mode,
            language=request.language
        )
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    """
    Summarizes study notes/text.
    """
    try:
        system_prompt = get_summary_prompt(request.language)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Text to summarize:\n\n{request.text}"}
        ]
        
        summary = await ask_llm(messages)
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error in /summarize endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
