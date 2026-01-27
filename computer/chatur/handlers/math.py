"""Math and Unit Conversion Handler"""

from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger
import simpleeval
import pint
from typing import Dict, Any, Optional

logger = setup_logger('chatur.handlers.math')

class MathHandler(BaseHandler):
    """Handler for calculations and unit conversions"""
    
    def __init__(self):
        self.ureg = pint.UnitRegistry()
        self.ureg.autoconvert_offset_to_baseunit = True  # Handle temps correctly
        
        # Configure simpleeval with safe math functions
        self.functions = simpleeval.DEFAULT_FUNCTIONS.copy()
        
        # Add basic math constants/funcs if needed, but simpleeval has defaults
        import math
        self.functions.update({
            'sqrt': math.sqrt,
            'pow': math.pow,
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'pi': math.pi,
            'e': math.e
        })
        
    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can process the intent"""
        return intent.type == IntentType.MATH
    
    def handle(self, intent: Intent) -> str:
        """Process math/conversion request"""
        try:
            operation = intent.parameters.get('operation')
            query = intent.parameters.get('query')
            
            if operation == 'calculate':
                return self._handle_calculation(query, intent.language)
            elif operation == 'convert':
                return self._handle_conversion(intent.parameters, intent.language)
            else:
                return "I'm not sure what calculation to perform."
                
        except Exception as e:
            logger.error(f"Math handling error: {e}")
            return "Sorry, I couldn't calculate that."

    def _handle_calculation(self, expression: str, language: str) -> str:
        """Evaluate mathematical expression safely"""
        if not expression:
            return "What would you like me to calculate?"
            
        try:
            # Clean up expression symbols for python
            # Replace common natural language math terms
            clean_expr = expression.lower()
            clean_expr = clean_expr.replace('plus', '+')
            clean_expr = clean_expr.replace('minus', '-')
            clean_expr = clean_expr.replace('times', '*')
            clean_expr = clean_expr.replace('multiplied by', '*')
            clean_expr = clean_expr.replace('x', '*')  # risky if variable, but likely multiplication in voice
            clean_expr = clean_expr.replace('divided by', '/')
            clean_expr = clean_expr.replace('over', '/')
            clean_expr = clean_expr.replace('^', '**')
            clean_expr = clean_expr.replace('power of', '**')
            
            # Remove non-math chars except allowed ones
            # This is a bit aggressive, might remove necessary chars
            # Better to reply on the extracted query from LLM being relatively clean
            
            result = simpleeval.simple_eval(clean_expr, functions=self.functions)
            
            # Format result
            if isinstance(result, float):
                # If integer, display as integer
                if result.is_integer():
                    result_str = str(int(result))
                else:
                    result_str = f"{result:.4f}".rstrip('0').rstrip('.')
            else:
                result_str = str(result)
                
            return f"The answer is {result_str}"
            
        except Exception as e:
            logger.warning(f"Calculation failed for '{expression}': {e}")
            return "I couldn't calculate that. Please check the expression."

    def _handle_conversion(self, params: Dict[str, Any], language: str) -> str:
        """Handle unit conversion using Pint"""
        try:
            source_value = params.get('value')
            source_unit = params.get('source_unit')
            target_unit = params.get('target_unit')
            
            if not source_value or not source_unit or not target_unit:
                return "I need the value and both units to convert."
                
            # Construct quantity
            qty = self.ureg(f"{source_value} {source_unit}")
            
            # Convert
            converted = qty.to(target_unit)
            
            # Format output (e.g. 10.5 km)
            result_val = converted.magnitude
            result_unit = converted.units
            
            if isinstance(result_val, float):
                 result_str = f"{result_val:.4f}".rstrip('0').rstrip('.')
            else:
                result_str = str(result_val)
                
            return f"{source_value} {source_unit} is {result_str} {result_unit}"
            
        except pint.UndefinedUnitError as e:
             return f"I don't recognize the unit '{e.unit_names}'"
        except Exception as e:
            logger.error(f"Conversion error: {e}")
            return "I couldn't perform that conversion."
