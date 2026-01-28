from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import yaml
from pathlib import Path
from chatur.utils.config import config

router = APIRouter()

class VoiceSettings(BaseModel):
    rate: int
    volume: float
    
class SettingsUpdate(BaseModel):
    tts: Optional[VoiceSettings] = None
    language: Optional[str] = None
    
@router.get("/config")
async def get_config():
    """Get current configuration"""
    # We return the loaded config object or re-read the file
    # For accuracy, let's read the file as the source of truth
    try:
        config_path = Path("config/config.yaml")
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {"error": "Config file not found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config")
async def update_config(settings: SettingsUpdate):
    """Update configuration"""
    try:
        config_path = Path("config/config.yaml")
        if not config_path.exists():
             raise HTTPException(status_code=404, detail="Config file not found")
             
        # Read existing
        with open(config_path, 'r', encoding='utf-8') as f:
            current_config = yaml.safe_load(f) or {}
            
        # Update values
        if settings.tts:
            if 'tts' not in current_config: current_config['tts'] = {}
            current_config['tts']['rate'] = settings.tts.rate
            current_config['tts']['volume'] = settings.tts.volume
            
        # Save back
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(current_config, f, default_flow_style=False)
            
        # Reload config in memory
        config.load_config()
        
        return {"status": "updated", "config": current_config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
