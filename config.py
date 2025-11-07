import os
from dotenv import load_dotenv
from config_manager import get_current_org_name, get_org_config, get_org_token_file

load_dotenv()

def get_current_config():
    """Get configuration for the current org"""
    org_name = get_current_org_name()
    if org_name:
        return get_org_config(org_name)
    return {}

# Load current org configuration
user_config = get_current_config()

# Try to get from user config first, fallback to .env
auth_config = user_config.get("auth", {})
LOGIN_URL = auth_config.get("login_url") or os.environ.get("LOGIN_URL")
CLIENT_ID = auth_config.get("client_id") or os.environ.get("CLIENT_ID")
CLIENT_SECRET = auth_config.get("client_secret") or os.environ.get("CLIENT_SECRET")
API_VERSION = auth_config.get("api_version") or os.environ.get("API_VERSION", "v62.0")

# Get org-specific token file
org_name = get_current_org_name()
if org_name:
    TOKEN_FILE = get_org_token_file(org_name)
else:
    TOKEN_FILE = os.environ.get("TOKEN_FILE", "access-token.secret")

DEFAULT_ML_MODEL = "llmgateway__VertexAIGemini20Flash001"

# Get schema from user config
SCHEMA_CONFIG = user_config.get("schema", {})