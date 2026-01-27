"""
Test script for Weather and System Info features
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("WEATHER & SYSTEM INFO TEST")
print("=" * 70)

# Test System Info (no API key needed)
print("\n" + "=" * 70)
print("SYSTEM INFORMATION TEST")
print("=" * 70)

try:
    from chatur.handlers.system_info import SystemInfoHandler
    from chatur.models.intent import Intent, IntentType
    
    handler = SystemInfoHandler()
    
    # Test battery
    print("\n1. Battery Info:")
    intent = Intent(
        type=IntentType.SYSTEM_INFO,
        language='en',
        parameters={'query_type': 'battery'},
        response_language='en'
    )
    response = handler.handle(intent)
    print(f"   {response}")
    
    # Test CPU
    print("\n2. CPU Info:")
    intent.parameters = {'query_type': 'cpu'}
    response = handler.handle(intent)
    print(f"   {response}")
    
    # Test Memory
    print("\n3. Memory Info:")
    intent.parameters = {'query_type': 'memory'}
    response = handler.handle(intent)
    print(f"   {response}")
    
    # Test Disk
    print("\n4. Disk Info:")
    intent.parameters = {'query_type': 'disk'}
    response = handler.handle(intent)
    print(f"   {response}")
    
    # Test Network
    print("\n5. Network Info:")
    intent.parameters = {'query_type': 'network'}
    response = handler.handle(intent)
    print(f"   {response}")
    
    print("\n[SUCCESS] System info handler working!")

except Exception as e:
    print(f"\n[ERROR] System info test failed: {e}")
    import traceback
    traceback.print_exc()

# Test Weather (requires API key)
print("\n" + "=" * 70)
print("WEATHER TEST")
print("=" * 70)

try:
    from chatur.integrations.weather import WeatherService
    
    weather_service = WeatherService()
    
    if not weather_service.api_key:
        print("\n[SKIP] OPENWEATHER_API_KEY not set")
        print("\nTo enable weather:")
        print("1. Get free API key from: https://openweathermap.org/api")
        print("2. Add to .env file:")
        print("   OPENWEATHER_API_KEY=your_key_here")
    else:
        print("\n1. Current Weather:")
        weather = weather_service.get_current_weather()
        if weather:
            print(f"   {weather_service.format_current_weather(weather)}")
            print("   [SUCCESS] Weather service working!")
        else:
            print("   [FAIL] Could not fetch weather")
        
        print("\n2. Forecast:")
        forecast = weather_service.get_forecast(days=3)
        if forecast:
            print(f"   {weather_service.format_forecast(forecast)}")
        else:
            print("   [FAIL] Could not fetch forecast")

except Exception as e:
    print(f"\n[ERROR] Weather test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
