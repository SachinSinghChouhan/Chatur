
from chatur.core.llm import LLMClient
from chatur.models.intent import IntentType

def test_intent_rules():
    client = LLMClient()
    
    test_cases = [
        ("check my mails", IntentType.EMAIL),
        ("read my email", IntentType.EMAIL),
        ("do i have any new emails", IntentType.EMAIL),
        ("search emails from boss", IntentType.EMAIL),
        ("remind me to buy milk", IntentType.TASK),
        ("add call mom to my list", IntentType.TASK),
        ("what are my tasks", IntentType.TASK),
        ("complete buy milk", IntentType.TASK),
        ("remove call mom from list", IntentType.TASK),
        ("remove what are my task from task list", IntentType.TASK), # Regression test
        ("what is the weather", IntentType.QUESTION), # Should fallback or be weather
        ("open google", IntentType.APP_LAUNCH)
    ]
    
    print("Testing Intent Rules...")
    print("-" * 30)
    
    passed = 0
    for text, expected in test_cases:
        intent = client.classify_intent(text)
        result = "PASS" if intent.type == expected else f"FAIL (Got {intent.type})"
        print(f"'{text}' -> {result}")
        if intent.type == expected:
            passed += 1
            
    print("-" * 30)
    print(f"Passed: {passed}/{len(test_cases)}")

if __name__ == "__main__":
    test_intent_rules()
