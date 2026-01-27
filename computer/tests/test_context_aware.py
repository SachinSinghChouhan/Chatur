"""
Test script for context-aware LLM capabilities
"""
import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatur.core.llm import LLMClient
from chatur.handlers.qa import QAHandler
from chatur.storage.conversation_repository import ConversationRepository
from chatur.models.intent import Intent, IntentType
from chatur.storage.init_db import init_database

def test_context_awareness():
    print("="*60)
    print("Testing Context-Aware LLM")
    print("="*60)
    
    # Setup test database
    import chatur.storage.repository
    import chatur.storage.init_db
    from pathlib import Path
    
    # Use a temporary file in the current directory
    TEST_DB = Path("test_computer.db")
    if TEST_DB.exists():
        os.remove(TEST_DB)
        
    print(f"Using test database: {TEST_DB.absolute()}")
    
    # Patch DB paths
    chatur.storage.repository.DB_PATH = TEST_DB
    chatur.storage.init_db.DB_PATH = TEST_DB
    
    # Initialize
    load_dotenv()
    init_database()
    
    try:
        llm = LLMClient()
        repo = ConversationRepository()
        handler = QAHandler(llm, repo)
        
        # create a unique session for testing
        session_id = "test_session_context"
        
        # 1. Simulate user stating a fact
        user_input_1 = "My name is Sachin."
        print(f"\nUser: {user_input_1}")
        
        # We need to manually add this to history effectively as if it was processed
        assistant_resp_1 = "Nice to meet you, Sachin."
        repo.add_exchange(user_input_1, assistant_resp_1, "question", session_id)
        print(f"Assistant (simulated): {assistant_resp_1}")
        
        # 2. Ask a follow-up question that relies on context
        user_input_2 = "What is my name?"
        print(f"\nUser: {user_input_2}")
        
        intent = Intent(
            type=IntentType.QUESTION,
            language='en',
            parameters={'question': user_input_2},
            response_language='en'
        )
        
        # The handler should now fetch history including the previous exchange
        response = handler.handle(intent)
        print(f"Assistant: {response}")
        
        # Validation
        if "Sachin" in response:
            print("\n[PASS] Context was successfully retrieved!")
        else:
            print("\n[FAIL] Context was not retrieved.")
            
    finally:
        # Cleanup
        if TEST_DB.exists():
            try:
                os.remove(TEST_DB)
                print("Test database cleaned up.")
            except PermissionError:
                print("Warning: Could not remove test database (file in use).")


if __name__ == "__main__":
    test_context_awareness()
