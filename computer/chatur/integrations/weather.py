"""
Weather integration using OpenWeatherMap API
"""

import os
import requests
from typing import Optional, Dict
from chatur.utils.logger import setup_logger
from chatur.utils.config import config

logger = setup_logger('chatur.integrations.weather')


class WeatherService:
    """Weather service using OpenWeatherMap API"""
    
    def __init__(self):
        """Initialize weather service"""
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
        # Default location (can be configured)
        self.default_city = config.get('weather.default_city', 'New York')
        self.units = config.get('weather.units', 'imperial')  # imperial, metric, standard
        
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY not set - weather features will not work")
    
    def get_current_weather(self, city: Optional[str] = None) -> Optional[Dict]:
        """
        Get current weather for a city
        
        Args:
            city: City name (uses default if None)
        
        Returns:
            Weather data dictionary or None if failed
        """
        if not self.api_key:
            logger.error("OpenWeather API key not configured")
            return None
        
        city = city or self.default_city
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            weather = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'wind_speed': round(data['wind']['speed']),
                'units': self.units
            }
            
            logger.info(f"Got weather for {city}: {weather['temperature']}°")
            return weather
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch weather: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse weather data: {e}")
            return None
    
    def get_forecast(self, city: Optional[str] = None, days: int = 3) -> Optional[list]:
        """
        Get weather forecast
        
        Args:
            city: City name (uses default if None)
            days: Number of days (max 5)
        
        Returns:
            List of forecast data or None if failed
        """
        if not self.api_key:
            logger.error("OpenWeather API key not configured")
            return None
        
        city = city or self.default_city
        days = min(days, 5)  # API limit
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': self.units,
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Group by day
            forecasts = []
            current_day = None
            day_data = []
            
            for item in data['list']:
                date = item['dt_txt'].split()[0]
                
                if date != current_day:
                    if day_data:
                        # Calculate daily summary
                        temps = [d['main']['temp'] for d in day_data]
                        forecasts.append({
                            'date': current_day,
                            'temp_min': round(min(temps)),
                            'temp_max': round(max(temps)),
                            'description': day_data[len(day_data)//2]['weather'][0]['description'],
                            'humidity': day_data[len(day_data)//2]['main']['humidity']
                        })
                    
                    current_day = date
                    day_data = [item]
                else:
                    day_data.append(item)
            
            # Add last day
            if day_data:
                temps = [d['main']['temp'] for d in day_data]
                forecasts.append({
                    'date': current_day,
                    'temp_min': round(min(temps)),
                    'temp_max': round(max(temps)),
                    'description': day_data[len(day_data)//2]['weather'][0]['description'],
                    'humidity': day_data[len(day_data)//2]['main']['humidity']
                })
            
            return forecasts[:days]
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch forecast: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse forecast data: {e}")
            return None
    
    def format_current_weather(self, weather: Dict) -> str:
        """
        Format current weather for speech
        
        Args:
            weather: Weather data dictionary
        
        Returns:
            Formatted weather string
        """
        temp_unit = "°F" if self.units == "imperial" else "°C"
        wind_unit = "mph" if self.units == "imperial" else "m/s"
        
        return (
            f"In {weather['city']}, it's currently {weather['temperature']}{temp_unit} "
            f"and {weather['description']}. "
            f"It feels like {weather['feels_like']}{temp_unit}. "
            f"Humidity is {weather['humidity']}%."
        )
    
    def format_forecast(self, forecasts: list) -> str:
        """
        Format forecast for speech
        
        Args:
            forecasts: List of forecast data
        
        Returns:
            Formatted forecast string
        """
        temp_unit = "°F" if self.units == "imperial" else "°C"
        
        lines = ["Here's the forecast:"]
        for forecast in forecasts:
            lines.append(
                f"{forecast['date']}: "
                f"{forecast['temp_min']} to {forecast['temp_max']}{temp_unit}, "
                f"{forecast['description']}"
            )
        
        return " ".join(lines)
