"""Weather handler"""

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.integrations.weather import WeatherService
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.handlers.weather')


class WeatherHandler(BaseHandler):
    """Handler for weather queries"""
    
    def __init__(self):
        self.weather_service = WeatherService()
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a weather intent"""
        return intent.type == IntentType.WEATHER
    
    def handle(self, intent: Intent) -> str:
        """Handle weather query"""
        try:
            query_type = intent.parameters.get('query_type', 'current')
            city = intent.parameters.get('city')
            
            if query_type == 'forecast':
                # Get forecast
                forecasts = self.weather_service.get_forecast(city)
                
                if not forecasts:
                    return "Sorry, I couldn't get the weather forecast right now"
                
                return self.weather_service.format_forecast(forecasts)
            
            else:
                # Get current weather
                weather = self.weather_service.get_current_weather(city)
                
                if not weather:
                    return "Sorry, I couldn't get the weather right now"
                
                return self.weather_service.format_current_weather(weather)
        
        except Exception as e:
            logger.error(f"Weather handler error: {e}", exc_info=True)
            return "Sorry, I had trouble getting the weather"
