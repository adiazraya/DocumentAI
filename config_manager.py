import json
import os
from typing import Dict, Any, List, Optional

ORGS_CONFIG_FILE = "orgs_config.json"

def load_orgs_config() -> Dict[str, Any]:
    """Load all org configurations from JSON file"""
    if os.path.exists(ORGS_CONFIG_FILE):
        try:
            with open(ORGS_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading orgs config: {e}")
    return {"orgs": {}, "current_org": None}

def save_orgs_config(config: Dict[str, Any]) -> bool:
    """Save all org configurations to JSON file"""
    try:
        with open(ORGS_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving orgs config: {e}")
        return False

def get_current_org_name(cookie_org: Optional[str] = None) -> Optional[str]:
    """Get the current org name from config or cookie"""
    config = load_orgs_config()
    
    # Priority: cookie > stored current_org > first org
    if cookie_org and cookie_org in config.get("orgs", {}):
        return cookie_org
    
    current = config.get("current_org")
    if current and current in config.get("orgs", {}):
        return current
    
    # Return first org if available
    orgs = config.get("orgs", {})
    if orgs:
        return list(orgs.keys())[0]
    
    return None

def set_current_org(org_name: str) -> bool:
    """Set the current active org"""
    config = load_orgs_config()
    if org_name not in config.get("orgs", {}):
        return False
    config["current_org"] = org_name
    return save_orgs_config(config)

def get_org_config(org_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific org"""
    config = load_orgs_config()
    orgs = config.get("orgs", {})
    
    if org_name is None:
        org_name = get_current_org_name()
    
    if org_name and org_name in orgs:
        return orgs[org_name]
    
    return None

def list_orgs() -> List[str]:
    """Get list of all configured org names"""
    config = load_orgs_config()
    return list(config.get("orgs", {}).keys())

def create_or_update_org(org_name: str, org_config: Dict[str, Any]) -> bool:
    """Create or update an org configuration"""
    config = load_orgs_config()
    if "orgs" not in config:
        config["orgs"] = {}
    
    config["orgs"][org_name] = org_config
    
    # If this is the first org, set it as current
    if config.get("current_org") is None:
        config["current_org"] = org_name
    
    return save_orgs_config(config)

def delete_org(org_name: str) -> bool:
    """Delete an org configuration"""
    config = load_orgs_config()
    orgs = config.get("orgs", {})
    
    if org_name not in orgs:
        return False
    
    del orgs[org_name]
    
    # If we deleted the current org, set a new one
    if config.get("current_org") == org_name:
        config["current_org"] = list(orgs.keys())[0] if orgs else None
    
    return save_orgs_config(config)

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

def get_org_token_file(org_name: str) -> str:
    """Get the token file path for a specific org"""
    return f"access-token-{org_name}.secret"

def initialize_config() -> Dict[str, Any]:
    """Initialize config with defaults from .env and schema.json"""
    from dotenv import load_dotenv
    load_dotenv()
    
    config = load_orgs_config()
    
    # If no orgs exist, create a default one from .env
    if not config.get("orgs"):
        default_org_name = "default"
        default_org_config = {
            "auth": {
                "login_url": os.environ.get("LOGIN_URL", ""),
                "client_id": os.environ.get("CLIENT_ID", ""),
                "client_secret": os.environ.get("CLIENT_SECRET", ""),
                "api_version": os.environ.get("API_VERSION", "v63.0")
            },
            "ml_model": "llmgateway__VertexAIGemini20Flash001",
            "datacloud_connector_name": "ContactIngestion",
            "datacloud_object_name": "LeadRecord",
            "schema": get_default_schema()
        }
        config["orgs"] = {default_org_name: default_org_config}
        config["current_org"] = default_org_name
        save_orgs_config(config)
    
    return config

# Legacy compatibility functions
def load_user_config() -> Dict[str, Any]:
    """Load current org's configuration (for backward compatibility)"""
    org_name = get_current_org_name()
    return get_org_config(org_name) or {}

def save_user_config(config: Dict[str, Any]) -> bool:
    """Save current org's configuration (for backward compatibility)"""
    org_name = get_current_org_name()
    if org_name:
        return create_or_update_org(org_name, config)
    return False

