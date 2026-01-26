"""
Quick test to verify Brave is now the default browser
"""

from chatur.core.llm import LLMClient

llm = LLMClient()

# Test cases
test_commands = [
    "open browser",
    "open brave",
    "open chrome",
    "launch browser",
    "kholo browser",
]

print("=" * 60)
print("BRAVE DEFAULT BROWSER TEST")
print("=" * 60)

for command in test_commands:
    intent = llm.classify_intent(command)
    app_name = intent.parameters.get('app_name', 'unknown')
    print(f"\nCommand: '{command}'")
    print(f"  → App: {app_name}")
    
    if 'browser' in command.lower() and 'chrome' not in command.lower():
        if app_name == 'brave':
            print("  [PASS] - Brave is default")
        else:
            print(f"  [FAIL] - Expected 'brave', got '{app_name}'")
    elif 'chrome' in command.lower():
        if app_name == 'chrome':
            print("  [PASS] - Chrome detected")
        else:
            print(f"  [FAIL] - Expected 'chrome', got '{app_name}'")
    elif 'brave' in command.lower():
        if app_name == 'brave':
            print("  [PASS] - Brave detected")
        else:
            print(f"  [FAIL] - Expected 'brave', got '{app_name}'")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
