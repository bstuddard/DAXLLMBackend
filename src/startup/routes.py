from src.startup.app import app
from src.startup.throttle import limiter
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from src.llm.anthropic_helpers import anthropic_stream_api_call, anthropic_full_api_call
from src.llm.schemas import ChatInput


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/stream")
@limiter.limit("5/second; 30/minute; 500/day")
async def stream_text(request: Request, input: ChatInput):
    """FastAPI endpoint to stream AI-generated text"""
    return StreamingResponse(anthropic_stream_api_call(input.chat_input_list), media_type="text/event-stream")


@app.post("/confidence")
@limiter.limit("5/second; 30/minute; 500/day")
async def get_confidence(request: Request, input: ChatInput):

    # Build conversation context and question
    chat_history = "\n".join([
        f"{msg['role']}: {msg['message']}"
        for msg in input.chat_input_list
    ])
    question = f"Given the following chat about DAX code, return a confidence score between 0 and 10 on how closely the user's question is answered by the DAX code provided by the helper as well as how correct the syntax appears to be:\n\n {chat_history}"
    chat_input_list = [
        {
            "role": "user",
            "message": question
        }
    ]

    # Make the AI Judge API call
    response = await anthropic_full_api_call(chat_input_list, "You are a judge of DAX code generation responses. You should only return full numbers and no other text allowed. Your response should be ONLY a single number between 0 and 10.")
    if not response:
        return {"score": "Unknown"}

    # Clean up the response - split by common patterns and get the last numeric part
    if ':' in response:
        response = response.split(':')[-1]
    if '\n' in response:
        response = response.split('\n')[-1]
    response = ''.join(filter(str.isdigit, response))  # Keep only digits
    
    if response.isdigit():
        score = int(response)
        if 0 <= score <= 10:
            return {"score": str(score)}
    return {"score": "Unknown"}


""" # Enable if needed for protected routes
from fastapi import Depends
from src.user.schemas import User
from src.user.user_jwt_interaction import get_user_from_auth_header

@app.get("/protected/")
async def protected_route(user_object: User = Depends(get_user_from_auth_header)):
    
    return {"username_parsed": str(user_object.username)}
"""

""" # Enable if needed for database queries
from src.startup.database import run_query

@app.get("/db_test/")
async def test_db():
    result = await run_query('SELECT id FROM stg.tbl WHERE id=1')
    return result[0]
"""
