"""File search handler for finding and opening files/folders"""

import os
import subprocess
import glob
from pathlib import Path
from typing import List, Optional
from chatur.handlers.base import BaseHandler
from chatur.models.intent import Intent, IntentType
from chatur.utils.logger import setup_logger
from chatur.utils.config import config
from chatur.utils.responses import ResponseBuilder

logger = setup_logger('chatur.handlers.file_search')

class FileSearchHandler(BaseHandler):
    """Handler for searching and opening files/folders"""
    
    def __init__(self) -> None:
        self.search_paths: List[str] = []
        for location in config.file_search_locations:
            expanded = os.path.expanduser(location)
            self.search_paths.append(expanded)
    
    def can_handle(self, intent: Intent) -> bool:
        """Check if this is a file search intent"""
        return intent.type == IntentType.FILE_SEARCH
    
    def handle(self, intent: Intent) -> str:
        """Search for and open file/folder"""
        try:
            query = intent.parameters.get('query', '').strip()
            language = intent.response_language
            
            if not query:
                return ResponseBuilder.ask(language, "What would you like to search for?")
            
            logger.info(f"Searching for: {query}")
            
            results = self._search_files(query)
            
            if not results:
                return ResponseBuilder.not_found(language, query)
            
            result_path = results[0]
            success = self._open_path(result_path)
            
            if success:
                result_name = os.path.basename(result_path)
                logger.info(f"Opened: {result_path}")
                return ResponseBuilder.success(language, "Opening", result_name)
            else:
                return ResponseBuilder.error(language, "open the file")
                
        except Exception as e:
            logger.error(f"File search error: {e}", exc_info=True)
            return ResponseBuilder.error(intent.response_language, "search for files")
    
    def _search_files(self, query: str, max_results: Optional[int] = None) -> List[str]:
        """Search for files/folders matching query"""
        if max_results is None:
            max_results = config.get_int('file_search.max_results', 5)
        
        results: List[str] = []
        query_lower = query.lower()
        
        try:
            # Search in common locations
            for search_path in self.search_paths:
                if not os.path.exists(search_path):
                    continue
                
                try:
                    # Use glob for pattern matching
                    pattern = f"**/*{query}*"
                    
                    for path in Path(search_path).glob(pattern):
                        if len(results) >= max_results:
                            break
                        
                        # Check if name matches
                        if query_lower in path.name.lower():
                            results.append(str(path))
                    
                    if len(results) >= max_results:
                        break
                        
                except (PermissionError, OSError):
                    # Skip directories we can't access
                    continue
            
            # Sort by relevance (exact matches first)
            results.sort(key=lambda p: (
                0 if query_lower == os.path.basename(p).lower() else 1,
                len(os.path.basename(p))
            ))
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def _open_path(self, path: str) -> bool:
        """Open file or folder"""
        try:
            os.startfile(path)
            return True
        except Exception as e:
            logger.error(f"Failed to open {path}: {e}")
            return False
