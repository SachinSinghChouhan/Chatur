"""Bilingual response utility to reduce duplication across handlers"""

from typing import Dict, Optional
from chatur.utils.logger import setup_logger

logger = setup_logger('chatur.utils.responses')


class ResponseBuilder:
    """Helper for building bilingual responses"""
    
    @staticmethod
    def get(lang: str, responses: Dict[str, str]) -> str:
        """
        Get response in the requested language.
        
        Args:
            lang: Language code ('en' or 'hi')
            responses: Dict with 'en' and/or 'hi' keys
            
        Returns:
            Response in requested language, fallback to English
        """
        if lang == 'hi' and 'hi' in responses:
            return responses['hi']
        return responses.get('en', '')
    
    @staticmethod
    def success(lang: str, action: str, item: Optional[str] = None) -> str:
        """Generate success response"""
        responses = {
            'en': f"Done: {action}" + (f" {item}" if item else ""),
            'hi': f"{action} हो गया" + (f" {item}" if item else "")
        }
        return ResponseBuilder.get(lang, responses)
    
    @staticmethod
    def error(lang: str, context: str) -> str:
        """Generate error response"""
        responses = {
            'en': f"Sorry, I couldn't {context}",
            'hi': f"माफ़ करें, {context} में समस्या हुई"
        }
        return ResponseBuilder.get(lang, responses)
    
    @staticmethod
    def not_found(lang: str, item: str) -> str:
        """Generate not found response"""
        responses = {
            'en': f"I couldn't find {item}",
            'hi': f"{item} नहीं मिला"
        }
        return ResponseBuilder.get(lang, responses)
    
    @staticmethod
    def confirm(lang: str, action: str) -> str:
        """Generate confirmation response"""
        responses = {
            'en': action,
            'hi': "ठीक है"
        }
        return ResponseBuilder.get(lang, responses)
    
    @staticmethod
    def ask(lang: str, question: str) -> str:
        """Generate ask question response"""
        responses = {
            'en': question,
            'hi': question
        }
        return ResponseBuilder.get(lang, responses)
