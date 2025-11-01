import json
import os
from typing import Dict, Any

USER_CONFIG_FILE = "user_config.json"

def load_user_config() -> Dict[str, Any]:
    """Load user configuration from JSON file"""
    if os.path.exists(USER_CONFIG_FILE):
        try:
            with open(USER_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user config: {e}")
    return {}

def save_user_config(config: Dict[str, Any]) -> bool:
    """Save user configuration to JSON file"""
    try:
        with open(USER_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user config: {e}")
        return False

def get_default_schema() -> Dict[str, Any]:
    """Load default schema from schema.json"""
    schema_file = "schema.json"
    if os.path.exists(schema_file):
        try:
            with open(schema_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading default schema: {e}")
    return {}

def initialize_config() -> Dict[str, Any]:
    """Initialize config with defaults from .env and schema.json"""
    from dotenv import load_dotenv
    load_dotenv()
    
    config = load_user_config()
    
    # If config is empty, initialize with defaults
    if not config:
        config = {
            "auth": {
                "login_url": os.environ.get("LOGIN_URL", ""),
                "client_id": os.environ.get("CLIENT_ID", ""),
                "client_secret": os.environ.get("CLIENT_SECRET", ""),
                "api_version": os.environ.get("API_VERSION", "v62.0")
            },
            "ml_model": "llmgateway__VertexAIGemini20Flash001",
            "datacloud_connector_name": "ContactIngestion",
            "datacloud_object_name": "LeadRecord",
            "schema": get_default_schema()
        }
        save_user_config(config)
    
    return config

