"""
Test URL and file opening functionality
"""

from chatur.core.llm import LLMClient
from chatur.models.intent import IntentType

llm = LLMClient()

# Test cases
test_commands = [
    # URL tests
    ("open youtube.com", IntentType.APP_LAUNCH, "youtube.com"),
    ("open google.com", IntentType.APP_LAUNCH, "google.com"),
    ("open github site", IntentType.APP_LAUNCH, "github.com"),
    ("open xyz site", IntentType.APP_LAUNCH, "xyz.com"),
    ("kholo facebook.com", IntentType.APP_LAUNCH, "facebook.com"),
    
    # File tests
    ("open report.pdf", IntentType.FILE_SEARCH, "report.pdf"),
    ("open document.docx", IntentType.FILE_SEARCH, "document.docx"),
    ("open photo.jpg", IntentType.FILE_SEARCH, "photo.jpg"),
    
    # App tests (should still work)
    ("open browser", IntentType.APP_LAUNCH, "brave"),
    ("open chrome", IntentType.APP_LAUNCH, "chrome"),
    ("open calculator", IntentType.APP_LAUNCH, "calculator"),
]

print("=" * 70)
print("URL AND FILE OPENING TEST")
print("=" * 70)

passed = 0
failed = 0

for command, expected_type, expected_value in test_commands:
    intent = llm.classify_intent(command)
    
    print(f"\nCommand: '{command}'")
    print(f"  Intent Type: {intent.type}")
    
    if intent.type == expected_type:
        if expected_type == IntentType.APP_LAUNCH:
            url = intent.parameters.get('url')
            app_name = intent.parameters.get('app_name')
            
            if url:
                print(f"  URL: {url}")
                if expected_value in url:
                    print("  [PASS] - URL detected correctly")
                    passed += 1
                else:
                    print(f"  [FAIL] - Expected '{expected_value}' in URL, got '{url}'")
                    failed += 1
            elif app_name:
                print(f"  App: {app_name}")
                if app_name == expected_value:
                    print("  [PASS] - App detected correctly")
                    passed += 1
                else:
                    print(f"  [FAIL] - Expected '{expected_value}', got '{app_name}'")
                    failed += 1
        
        elif expected_type == IntentType.FILE_SEARCH:
            query = intent.parameters.get('query')
            print(f"  File: {query}")
            if query == expected_value:
                print("  [PASS] - File detected correctly")
                passed += 1
            else:
                print(f"  [FAIL] - Expected '{expected_value}', got '{query}'")
                failed += 1
    else:
        print(f"  [FAIL] - Expected type '{expected_type}', got '{intent.type}'")
        failed += 1

print("\n" + "=" * 70)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 70)
