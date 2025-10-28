import yaml
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration management"""
    
    def __init__(self, config_path: Path = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        
        with open(config_path, 'r') as f:
            self.data = yaml.safe_load(f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    @property
    def openai_config(self) -> Dict[str, Any]:
        return self.data.get('openai', {})
    
    @property
    def processing_config(self) -> Dict[str, Any]:
        return self.data.get('processing', {})
    
    @property
    def output_config(self) -> Dict[str, Any]:
        return self.data.get('output', {})
    
    @property
    def evaluation_config(self) -> Dict[str, Any]:
        return self.data.get('evaluation', {})
