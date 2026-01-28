from fastapi import APIRouter, HTTPException, Query
from chatur.storage.conversation_repository import ConversationRepository
from typing import List, Dict

router = APIRouter()
conversation_repo = ConversationRepository()

@router.get("/history")
async def get_history(limit: int = Query(default=50, le=100)):
    """Get recent command history"""
    try:
        # get_recent_exchanges returns oldest first, but for history UI we usually want newest first
        # The repo method sorts by timestamp DESC then reverses it. 
        # We can just reverse it back or modify the repo. Reversing here is easier.
        history = conversation_repo.get_recent_exchanges(limit=limit)
        return list(reversed(history))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
