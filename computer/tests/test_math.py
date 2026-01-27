"""
Test script for Math and Unit Conversion
"""
import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatur.handlers.math import MathHandler
from chatur.models.intent import Intent, IntentType

def test_math_handler():
    print("="*60)
    print("Testing Math Handler (Calculator & Unit Converter)")
    print("="*60)
    
    handler = MathHandler()
    
    # Test 1: Simple Calculation
    print("\n--- Test 1: Calculation ---")
    intent_calc = Intent(
        type=IntentType.MATH,
        language='en',
        parameters={'operation': 'calculate', 'query': '25 * 4 + 10'},
        response_language='en'
    )
    result_calc = handler.handle(intent_calc)
    print(f"Query: 25 * 4 + 10")
    print(f"Result: {result_calc}")
    
    if "110" in result_calc:
        print("[PASS] Calculation correct")
    else:
        print(f"[FAIL] Calculation incorrect: {result_calc}")
        
    # Test 2: Unit Conversion
    print("\n--- Test 2: Unit Conversion (Length) ---")
    intent_conv = Intent(
        type=IntentType.MATH,
        language='en',
        parameters={
            'operation': 'convert',
            'value': 100,
            'source_unit': 'miles',
            'target_unit': 'kilometers'
        },
        response_language='en'
    )
    result_conv = handler.handle(intent_conv)
    print(f"Query: 100 miles -> kilometers")
    print(f"Result: {result_conv}")
    
    # 100 miles is approx 160.934 km
    if "160.9" in result_conv:
        print("[PASS] Conversion correct")
    else:
        print(f"[FAIL] Conversion incorrect: {result_conv}")

    # Test 3: Unit Conversion (Temperature)
    print("\n--- Test 3: Unit Conversion (Temperature) ---")
    intent_temp = Intent(
        type=IntentType.MATH,
        language='en',
        parameters={
            'operation': 'convert',
            'value': 32,
            'source_unit': 'fahrenheit',
            'target_unit': 'celsius'
        },
        response_language='en'
    )
    result_temp = handler.handle(intent_temp)
    print(f"Query: 32 F -> C")
    print(f"Result: {result_temp}")
    
    # 32F is 0C
    if "0" in result_temp or "0.0" in result_temp:
        print("[PASS] Temperature conversion correct")
    else:
        print(f"[FAIL] Temperature conversion incorrect: {result_temp}")

if __name__ == "__main__":
    test_math_handler()
