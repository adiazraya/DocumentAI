import os
from dotenv import load_dotenv
from config_manager import load_user_config

load_dotenv()

# Load user configuration
user_config = load_user_config()

# Try to get from user config first, fallback to .env
auth_config = user_config.get("auth", {})
LOGIN_URL = auth_config.get("login_url") or os.environ.get("LOGIN_URL")
CLIENT_ID = auth_config.get("client_id") or os.environ.get("CLIENT_ID")
CLIENT_SECRET = auth_config.get("client_secret") or os.environ.get("CLIENT_SECRET")
API_VERSION = auth_config.get("api_version") or os.environ.get("API_VERSION", "v62.0")
TOKEN_FILE = os.environ.get("TOKEN_FILE", "access-token.secret")

DEFAULT_ML_MODEL = "llmgateway__VertexAIGemini20Flash001"

# Get schema from user config
SCHEMA_CONFIG = user_config.get("schema", {})