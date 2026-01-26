"""Test file search"""
import sys
sys.path.insert(0, '.')

from chatur.core.llm import LLMClient

llm = LLMClient()

tests = [
    'search for computer',
    'find test.txt',
    'locate downloads folder',
    'protocol dhundo',
]

print("Testing file search intent:")
print("=" * 60)

for cmd in tests:
    intent = llm.classify_intent(cmd)
    print(f"{cmd:30} → {intent.type.value:15} query: {intent.parameters.get('query', 'N/A')}")

print("=" * 60)
