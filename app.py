from flask import Flask, request, jsonify, render_template, send_file, redirect, render_template_string
import subprocess
import json
import requests
import base64
import logging
import os
import uuid
from datetime import datetime, timezone

# Import configuration
from config import DEFAULT_ML_MODEL, LOGIN_URL, CLIENT_ID, CLIENT_SECRET, API_VERSION, TOKEN_FILE, SCHEMA_CONFIG
from api_client import APIClient
from config_manager import load_user_config, save_user_config, initialize_config, get_default_schema

app = Flask("Salesforce Data Cloud Document AI test platform")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize API client
api_client = APIClient()

# Helper function to get Data Cloud token
def get_datacloud_token(salesforce_access_token, instance_url):
    """Exchange Salesforce token for Data Cloud token"""
    try:
        token_url = f"https://{instance_url}/services/a360/token"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'urn:salesforce:grant-type:external:cdp',
            'subject_token': salesforce_access_token,
            'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token'
        }
        
        # Debug output
        logging.info("=" * 80)
        logging.info("DATA CLOUD TOKEN EXCHANGE REQUEST")
        logging.info("=" * 80)
        logging.info(f"Token URL: {token_url}")
        logging.info(f"Headers: {json.dumps(headers, indent=2)}")
        logging.info(f"Request Body:")
        logging.info(f"  grant_type: {data['grant_type']}")
        logging.info(f"  subject_token: {salesforce_access_token[:20]}...{salesforce_access_token[-20:] if len(salesforce_access_token) > 40 else ''}")
        logging.info(f"  subject_token_type: {data['subject_token_type']}")
        logging.info("=" * 80)
        
        response = requests.post(token_url, headers=headers, data=data, timeout=30)
        
        # Debug output
        logging.info("DATA CLOUD TOKEN EXCHANGE RESPONSE")
        logging.info("=" * 80)
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            token_data = response.json()
            logging.info("Response Body:")
            logging.info(f"  access_token: {token_data['access_token'][:30]}...{token_data['access_token'][-20:] if len(token_data['access_token']) > 50 else ''}")
            logging.info(f"  instance_url: {token_data['instance_url']}")
            logging.info(f"  token_type: {token_data.get('token_type', 'N/A')}")
            logging.info(f"  expires_in: {token_data.get('expires_in', 'N/A')} seconds")
            logging.info("Successfully obtained Data Cloud token")
            logging.info("=" * 80)
            return {
                'access_token': token_data['access_token'],
                'instance_url': token_data['instance_url']
            }
        else:
            logging.error(f"Response Body: {response.text}")
            logging.error(f"Failed to get Data Cloud token: {response.status_code}")
            logging.info("=" * 80)
            return None
            
    except Exception as e:
        logging.error(f"Exception during token exchange: {str(e)}")
        logging.info("=" * 80)
        return None

# Helper function to extract values from nested type/value structure
def extract_value(obj):
    """Recursively extract values from type/value structure"""
    if obj and isinstance(obj, dict) and 'type' in obj and 'value' in obj:
        if obj['type'] == 'array' and isinstance(obj['value'], list):
            return [extract_value(item) for item in obj['value']]
        elif obj['type'] == 'object' and isinstance(obj['value'], dict):
            extracted = {}
            for key, val in obj['value'].items():
                extracted[key] = extract_value(val)
            return extracted
        else:
            return obj['value']
    return obj

# Helper function to ingest data into Data Cloud
def ingest_to_datacloud(data, dc_token, dc_instance_url, connector_name="ContactIngestion", object_name="LeadRecord"):
    """Ingest extracted data into Salesforce Data Cloud"""
    try:
        # Extract clean values
        clean_data = {}
        for key, value in data.items():
            clean_data[key] = extract_value(value)
        
        # Get the array data (assuming it's LeadsTable or similar)
        leads_data = None
        for key, value in clean_data.items():
            if isinstance(value, list):
                leads_data = value
                break
        
        if not leads_data:
            logging.warning("No array data found for ingestion")
            return None
        
        # Prepare records for ingestion
        records = []
        for lead in leads_data:
            record = {
                "EventID": str(uuid.uuid4()),
                "eventime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            }
            # Add all fields from the lead
            record.update(lead)
            records.append(record)
        
        # Prepare ingestion payload with correct path structure
        ingestion_url = f"https://{dc_instance_url}/api/v1/ingest/sources/{connector_name}/{object_name}"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {dc_token}'
        }
        
        payload = {
            "data": records
        }
        
        # Debug output
        logging.info("=" * 80)
        logging.info("DATA CLOUD INGESTION REQUEST")
        logging.info("=" * 80)
        logging.info(f"Ingestion URL: {ingestion_url}")
        logging.info(f"Connector Name: {connector_name}")
        logging.info(f"Object Name: {object_name}")
        logging.info(f"Records to ingest: {len(records)}")
        logging.info(f"Headers:")
        logging.info(f"  Content-Type: {headers['Content-Type']}")
        logging.info(f"  Authorization: Bearer {dc_token[:30]}...{dc_token[-20:] if len(dc_token) > 50 else ''}")
        logging.info(f"Payload:")
        logging.info(json.dumps(payload, indent=2))
        logging.info("=" * 80)
        
        response = requests.post(ingestion_url, headers=headers, json=payload, timeout=30)
        
        # Debug output
        logging.info("DATA CLOUD INGESTION RESPONSE")
        logging.info("=" * 80)
        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Headers: {dict(response.headers)}")
        logging.info(f"Response Body: {response.text}")
        logging.info("=" * 80)
        
        if response.status_code in [200, 201, 202]:
            logging.info("✓ Data successfully ingested to Data Cloud")
            return {
                'success': True,
                'records_ingested': len(records),
                'response': response.json() if response.text else {}
            }
        else:
            logging.error(f"✗ Data Cloud ingestion failed: {response.status_code}")
            return {
                'success': False,
                'error': response.text,
                'status_code': response.status_code
            }
            
    except Exception as e:
        logging.error(f"Exception during Data Cloud ingestion: {str(e)}")
        logging.info("=" * 80)
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def check_auth_status():
    """Check authentication status"""
    try:
        has_token = api_client.is_authenticated()
        
        return jsonify({
            'serverTime': datetime.now().isoformat(),
            'status': 'running',
            'authenticated': has_token,
            'message': 'Access token found' if has_token else 'Access token not found. Please authenticate first.'
        })
    except Exception as e:
        return jsonify({
            'serverTime': datetime.now().isoformat(),
            'status': 'error',
            'authenticated': False,
            'error': 'Failed to check authentication status',
            'details': str(e)
        }), 500

@app.route('/api/auth-info', methods=['GET'])
def get_auth_info():
    """Get authentication configuration"""
    if not LOGIN_URL or not CLIENT_ID:
        return jsonify({'error': 'Salesforce config missing on server'}), 500
    
    return jsonify({
        'loginUrl': LOGIN_URL,
        'clientId': CLIENT_ID,
    })

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided in callback.", 400

    # Render a page that grabs code_verifier from sessionStorage and POSTs it to /auth/exchange
    # Check if user came from home page (based on referrer or can be made explicit)
    return render_template_string("""
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; 
                       border-radius: 50%; width: 40px; height: 40px; 
                       animation: spin 1s linear infinite; margin: 20px auto; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <h2>🔐 Completing Authentication...</h2>
        <div class="spinner"></div>
        <p>Please wait while we complete your authentication.</p>
        <script>
        const codeVerifier = sessionStorage.getItem('pkce_code_verifier');
        fetch('/auth/exchange', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ code: '{{code}}', code_verifier: codeVerifier })
        }).then(response => {
            if (response.ok) {
                // Check if came from home page
                const urlParams = new URLSearchParams(window.location.search);
                const returnPath = sessionStorage.getItem('auth_return_path') || '/config';
                sessionStorage.removeItem('auth_return_path');
                window.location = returnPath;
            } else {
                document.body.innerHTML = '<h2 style="color: red;">Authentication Failed</h2><p>Please try again.</p><a href="/">Return to Home</a>';
            }
        }).catch(error => {
            document.body.innerHTML = '<h2 style="color: red;">Authentication Error</h2><p>' + error.message + '</p><a href="/">Return to Home</a>';
        });
        </script>
    </body>
    </html>
    """, code=code)

@app.route('/auth/exchange', methods=['POST'])
def auth_exchange():
    data = request.get_json()
    code = data.get('code')
    code_verifier = data.get('code_verifier')
    if not code or not code_verifier:
        return "Missing code or code_verifier", 400

    redirect_uri = f"{request.url_root.rstrip('/')}/auth/callback"
    token_url = f"https://{LOGIN_URL}/services/oauth2/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier
    }

    print("Token exchange payload:", payload)
    print("Token URL:", token_url)
    
    resp = requests.post(token_url, data=payload)
    print("Response status:", resp.status_code)
    print("Response headers:", resp.headers)
    print("Response text:", resp.text)
    
    if resp.status_code != 200:
        return f"Error exchanging code for token: {resp.text}", 400

    token_data = resp.json()
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "access_token": token_data["access_token"],
            "instance_url": token_data["instance_url"]
        }, f)

    return '', 204

@app.route('/api/save-token', methods=['POST'])
def save_token():
    """Save access token from OAuth callback"""
    try:
        data = request.get_json()
        access_token = data.get('accessToken')
        
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Access token is required'
            }), 400
        
        # Save the access token
        api_client.save_access_token(access_token)
        
        print('Access token saved successfully')
        
        return jsonify({
            'success': True,
            'message': 'Access token saved successfully'
        })
    except Exception as e:
        print(f'Error saving access token: {e}')
        return jsonify({
            'success': False,
            'error': 'Failed to save access token',
            'details': str(e)
        }), 500

@app.route('/extract-data', methods=['POST'])
def extract_data():
    try:
        if not api_client.is_authenticated():
            return jsonify({'error': 'Authentication required. Please authenticate with Salesforce first.'}), 401

        ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed types are: PDF and images (PNG, JPG, JPEG, TIFF, BMP)'}), 400

        # Load schema and ML model from configuration
        config = load_user_config()
        schema_obj = config.get('schema', get_default_schema())
        ml_model = config.get('ml_model', DEFAULT_ML_MODEL)
        
        if not schema_obj:
            return jsonify({'error': 'No schema configured. Please configure a schema in the Configuration page.'}), 400
        
        file_data = file.read()
        base64_data = base64.b64encode(file_data).decode('utf-8')

        # Use dynamic instance_url from token file
        instance_url = api_client.get_instance_url()
        url = f"{instance_url}/services/data/{API_VERSION}/ssot/document-processing/actions/extract-data"

        payload = {
            "mlModel": ml_model,
            "schemaConfig": json.dumps(schema_obj),
            "files": [
                {
                    "mimeType": file.content_type or "image/jpeg",
                    "data": base64_data
                }
            ]
        }

        access_token = api_client.get_access_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        logging.info(f"Using ML model: {ml_model}")
        logging.info(f"Using schema: {payload['schemaConfig']}")
        
        response = requests.request("POST", url, headers=headers, json=payload, timeout=160)
            
        if response.status_code in [200, 201]:
            try:
                # Log raw response for debugging
                logging.debug(f"Raw response: {response.text}")
                
                json_response = response.json()
                logging.debug(f"JSON response: {json.dumps(json_response, indent=2)}")
                
                # Check if response has expected structure
                if not json_response:
                    return jsonify({'error': 'Empty response from server'}), 200
                
                if 'data' not in json_response or not json_response['data']:
                    return jsonify({'error': 'No data in response'}), 200
                
                # Check for error in the response
                if json_response['data'][0].get('error'):
                    error_msg = json_response['data'][0]['error']
                    if '403' in error_msg:
                        return jsonify({
                            'error': 'Authentication error with the OpenAI service. Please check your API credentials.',
                            'details': error_msg
                        }), 403
                    return jsonify({
                        'error': 'Service error',
                        'details': error_msg
                    }), 500
                
                nested_json_str = json_response['data'][0].get('data')
                if not nested_json_str:
                    return jsonify({'error': 'No extracted data in response'}), 200
                
                # Replace HTML entities
                nested_json_str = nested_json_str.replace('&quot;', '"').replace('&#92;', '\\')
                
                # Parse the JSON string
                nested_json = json.loads(nested_json_str)
                
                # Try to ingest to Data Cloud
                ingestion_result = None
                try:
                    # Get Data Cloud token
                    dc_credentials = get_datacloud_token(access_token, instance_url.replace('https://', '').replace('http://', ''))
                    
                    if dc_credentials:
                        # Get connector and object names from config
                        connector_name = config.get('datacloud_connector_name', 'ContactIngestion')
                        object_name = config.get('datacloud_object_name', 'LeadRecord')
                        
                        # Ingest data
                        ingestion_result = ingest_to_datacloud(
                            nested_json,
                            dc_credentials['access_token'],
                            dc_credentials['instance_url'],
                            connector_name,
                            object_name
                        )
                        
                        if ingestion_result and ingestion_result.get('success'):
                            logging.info(f"✓ Successfully ingested {ingestion_result.get('records_ingested', 0)} records to Data Cloud")
                        else:
                            logging.warning(f"✗ Data Cloud ingestion failed: {ingestion_result.get('error', 'Unknown error')}")
                    else:
                        logging.warning("✗ Could not obtain Data Cloud token, skipping ingestion")
                        
                except Exception as ingest_error:
                    logging.error(f"✗ Exception during Data Cloud ingestion: {str(ingest_error)}")
                    # Don't fail the main request if ingestion fails
                
                # Prepare response with ingestion status
                response_data = nested_json.copy()
                if ingestion_result:
                    response_data['_ingestion_status'] = ingestion_result
                
                # Convert the nested JSON to a string with proper encoding
                formatted_json = json.dumps(response_data, ensure_ascii=False, indent=2)
                
                return formatted_json, 200, {
                    'Content-Type': 'application/json; charset=utf-8'
                }
            except (KeyError, IndexError, json.JSONDecodeError) as e:
                return jsonify({
                    'error': f'Error processing response: {str(e)}',
                    'raw_response': response.text
                }), 500
        else:
            return jsonify({
                'error': f'API request failed with status {response.status_code}',
                'details': response.text
            }), response.status_code

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/json-jazz')
def json_jazz():
    return render_template('json-jazz.html')

@app.route('/config', methods=['GET'])
def config_page():
    """Configuration page"""
    return render_template('config.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    try:
        config = load_user_config()
        
        # If config is empty, initialize with defaults
        if not config:
            config = initialize_config()
        
        # Don't send sensitive data to frontend
        response_config = {
            'auth': {
                'login_url': config.get('auth', {}).get('login_url', ''),
                'client_id': config.get('auth', {}).get('client_id', ''),
                'client_secret': config.get('auth', {}).get('client_secret', ''),
                'api_version': config.get('auth', {}).get('api_version', 'v62.0')
            },
            'ml_model': config.get('ml_model', DEFAULT_ML_MODEL),
            'datacloud_connector_name': config.get('datacloud_connector_name', 'ContactIngestion'),
            'datacloud_object_name': config.get('datacloud_object_name', 'LeadRecord'),
            'schema': config.get('schema', {})
        }
        
        return jsonify(response_config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    """Save configuration"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No configuration data provided'}), 400
        
        # Validate schema if provided
        if 'schema' in data:
            if not isinstance(data['schema'], dict):
                return jsonify({'error': 'Schema must be a valid JSON object'}), 400
        
        # Save configuration
        success = save_user_config(data)
        
        if success:
            # Reload config module to pick up new values
            import importlib
            import config
            importlib.reload(config)
            
            return jsonify({'success': True, 'message': 'Configuration saved successfully'})
        else:
            return jsonify({'error': 'Failed to save configuration'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config/reset', methods=['POST'])
def reset_config():
    """Reset configuration to defaults"""
    try:
        config = initialize_config()
        
        # Reload config module
        import importlib
        import config as config_module
        importlib.reload(config_module)
        
        return jsonify({'success': True, 'message': 'Configuration reset to defaults'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/schema', methods=['GET'])
def get_schema():
    """Get current schema configuration"""
    try:
        config = load_user_config()
        schema = config.get('schema', get_default_schema())
        return jsonify(schema)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize configuration on startup
    initialize_config()
    
    # Get port from environment variable (for Heroku) or default to 3000
    port = int(os.environ.get("PORT", 3000))
    
    # Get debug mode from environment variable
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    # Host 0.0.0.0 allows external connections (required for Heroku)
    app.run(host="0.0.0.0", port=port, debug=debug)