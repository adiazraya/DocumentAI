import os
import json
from typing import Optional
from config_manager import get_current_org_name, get_org_token_file

class APIClient:
    def __init__(self, org_name: Optional[str] = None):
        self.org_name = org_name or get_current_org_name()
        self.token_file = get_org_token_file(self.org_name) if self.org_name else "access-token.secret"
    
    def set_org(self, org_name: str):
        """Switch to a different org"""
        self.org_name = org_name
        self.token_file = get_org_token_file(org_name)
    
    def load_token_data(self):
        if not os.path.exists(self.token_file):
            raise Exception('Token file not found. Please authenticate.')
        with open(self.token_file, 'r') as f:
            return json.load(f)
    
    def get_access_token(self):
        return self.load_token_data().get('access_token')
    
    def get_instance_url(self):
        return self.load_token_data().get('instance_url')
    
    def is_authenticated(self):
        try:
            data = self.load_token_data()
            return bool(data.get('access_token')) and bool(data.get('instance_url'))
        except Exception:
            return False
    
    def save_access_token(self, access_token: str) -> None:
        """Save access token to local storage"""
        with open(self.token_file, 'w') as f:
            f.write(access_token.strip()) 