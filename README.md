# Salesforce Data Cloud - Document AI API Testbed

## Introduction

This project provides a sample implementation demonstrating how to use the Salesforce Data Cloud Document AI APIs. It creates a simple web interface that allows users to upload documents (PDFs or images) along with a JSON schema, and then processes these documents using Salesforce's document extraction capabilities.

The application showcases how to:
- Make authenticated API calls to Salesforce Data Cloud Document AI endpoints using OAuth 2.0
- Process document uploads and convert them to base64 encoding
- Submit documents for intelligent extraction with custom schema configurations
- Display the extracted structured data from documents

This testbed serves as a reference implementation for developers looking to integrate Salesforce Data Cloud's document processing capabilities into their own applications.

Youtube video walkthrough: https://youtu.be/H8cgvUP7Ytg

## Project Structure

```
sf-datacloud-idp-testbed/
├── app.py                     # Main Flask application with Data Cloud ingestion
├── config.py                  # Configuration settings (API URLs, OAuth settings)
├── config_manager.py          # Configuration management utilities
├── api_client.py              # API client for token management
├── schema.json                # Default JSON schema for document extraction
├── OpenAPISpec.yaml           # Data Cloud ingestion schema definition
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── CONFIGURATION_GUIDE.md     # Detailed configuration guide
├── DATACLOUD_INGESTION.md     # Data Cloud integration documentation
├── static/                    # Static assets
│   ├── css/                   # CSS stylesheets
│   │   └── style.css          # Main stylesheet
│   ├── js/                    # JavaScript files
│   │   └── script.js          # Client-side functionality with camera support
│   └── json-jazz.html         # JSON Schema Generator tool
├── templates/                 # HTML templates
│   ├── index.html             # Main interface page with camera capture
│   └── config.html            # Configuration page with Data Cloud settings
└── .env.example               # Example environment file
```

## Environment Setup

1. **Clone the Repository**
    ```bash
    git clone https://github.com/ananth-anto/sf-datacloud-idp-testbed
    cd sf-datacloud-idp-testbed
    ```

2. **Create Environment File**
    ```bash
    cp .env.example .env
    ```

3. **Configure Salesforce Connected App**
    - Follow the [Setting Up External Client App guide](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_authenticate.htm&type=5)
    - **Important:** Use callback URL as `http://localhost:3000/auth/callback`
    - Copy your `ClientId`, `ClientSecret`, and `LoginUrl` from your Salesforce Connected App to your `.env` file

    Example `.env`:
    ```env
    LOGIN_URL=your-salesforce-login-url
    CLIENT_ID=your-salesforce-connected-app-client-id
    CLIENT_SECRET=your-salesforce-connected-app-client-secret
    API_VERSION=vXX.X
    TOKEN_FILE=access-token.secret
    ```

4. **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

5. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the Application**
    ```bash
    python app.py
    ```
    - The application will start and be available at `http://localhost:3000/` in your web browser.

---

## Using the Application

### Quick Start Guide

#### First-Time Setup (Configuration Page)

All setup is now done through the **Configuration Page** for a better user experience:

1. **Open Application**: Navigate to `http://localhost:3000`
2. **Go to Configuration**: Click the **⚙️ Configuration** button in the top-right corner
3. **Configure Authentication**: 
   - Enter your Salesforce LOGIN_URL (e.g., `login.salesforce.com`)
   - Enter CLIENT_ID (Consumer Key from Connected App)
   - Enter CLIENT_SECRET (Consumer Secret from Connected App)
   - Set API_VERSION (default: `v62.0`)
4. **Select ML Model**: Choose between:
   - **Gemini 2.0 Flash** - Fast and efficient processing
   - **OpenAI GPT-4o** - High accuracy results
5. **Configure Schema**: Edit the JSON schema to match your document extraction needs
6. **Save Configuration**: Click "💾 Save Configuration"
7. **Authenticate**: Click "🔐 Authenticate with Salesforce" and complete the OAuth flow
8. **Done!** You'll be redirected back with authentication confirmed

**Note**: The configuration page creates a `user_config.json` file that takes priority over `.env` variables. This file is automatically excluded from version control.

For detailed configuration instructions, see [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md).

### Document Processing Workflow

Once configured and authenticated:

1. **Upload or Capture Document**: 
   - **📷 Take Photo**: Click to use your device camera (great for mobile!)
   - **Upload File**: Choose from your device (PDF, PNG, JPG, JPEG, TIFF, BMP)
2. **Process**: Click "Analyze Document" 
3. **View Results**: All data is displayed in clean, professional tables:
   - **Summary Table**: Non-array fields shown first (e.g., Event name, Date)
   - **Data Tables**: Array data rendered with:
     - Color-coded headers
     - Alternating row colors for easy reading
     - Hover effects for better interactivity
   - **No JSON**: Everything is in table format for easy reading
4. **Configuration**: Uses your saved ML model and schema automatically

### Authentication Flow (OAuth 2.0 Web Server Flow)

Authentication is now managed entirely from the Configuration page:

1. **Configure Credentials**: Set up your Salesforce Connected App details in Configuration page
2. **Select ML Model**: Choose your preferred AI model for processing
3. **Save Configuration**: Persist your credentials and settings
4. **Click Authenticate**: Redirects to Salesforce login page
5. **Login & Authorize**: Enter credentials and grant permissions
6. **Return**: Redirected back to Configuration page with success confirmation
7. **Ready to Use**: Return to home page and start processing documents

## Camera Capture Feature

The application supports direct camera capture for easy document scanning:

### How to Use Camera
1. Click **📷 Take Photo** button
2. Allow camera permissions when prompted
3. Position your document in the camera view
4. Click **✓ Capture** to take the photo
5. The captured image is automatically added for processing

### Camera Benefits
- 📱 Perfect for mobile devices
- 📄 Quick document scanning on the go
- 🎯 Real-time preview before capture
- ✅ Automatic file handling

## Data Cloud Integration

The application automatically ingests extracted data into Salesforce Data Cloud:

### Automatic Ingestion
- ☁️ **Seamless Integration**: Extracted data automatically flows to Data Cloud
- 🔄 **Token Exchange**: Automatic conversion of Salesforce token to Data Cloud token
- 📊 **Real-time Processing**: Data ingested immediately after extraction
- ✅ **Status Tracking**: Ingestion success/failure reported in results

### Configuration
1. Go to **⚙️ Configuration** page
2. Find **☁️ Data Cloud Ingestion** section
3. Enter your **Data Cloud Connector Name** (e.g., `ContactIngestion`)
4. Enter your **Data Cloud Object Name** (e.g., `LeadRecord`)
5. Save configuration

**API Path Format**: `api/v1/ingest/sources/{connector_name}/{object_name}`

### What Gets Ingested
- All extracted array data (e.g., LeadsTable)
- Automatic UUID for each record (EventID)
- Automatic timestamp (eventime)
- All extracted fields from the document

### Response Format
Results include ingestion status:
```json
{
  "Evento": {...},
  "LeadsTable": [...],
  "_ingestion_status": {
    "success": true,
    "records_ingested": 2
  }
}
```

For detailed information, see [DATACLOUD_INGESTION.md](DATACLOUD_INGESTION.md).

## Results Display - Pure Tabular Format

All results are displayed in clean, professional tables - **NO JSON format**:

### Smart Table Formatting
- **Summary Information Table**: Single-value fields displayed in a 2-column table
  - Left column: Field name (bolded)
  - Right column: Field value
- **Data Tables**: Array data automatically converted to full tables with headers
- **No Raw JSON**: Everything is formatted for easy human reading

### Example Output Structure
```
Summary Information
┌─────────────┬──────────────────┐
│ Field       │ Value            │
├─────────────┼──────────────────┤
│ Evento      │ Tech Summit 2025 │
│ Date        │ 01/11/2025       │
└─────────────┴──────────────────┘

LeadsTable
┌────────────┬───────────┬──────────────────┬────────────┬──────────┐
│ Firstname  │ Lastname  │ Email            │ Date       │ Company  │
├────────────┼───────────┼──────────────────┼────────────┼──────────┤
│ John       │ Doe       │ john@example.com │ 01/11/2025 │ Acme Inc │
│ Jane       │ Smith     │ jane@example.com │ 02/11/2025 │ TechCorp │
└────────────┴───────────┴──────────────────┴────────────┴──────────┘
```

### Table Features
- 🎨 Color-coded headers with professional styling
- 📊 Alternating row colors for easy reading
- 🖱️ Hover effects for better interactivity
- 📱 Responsive design that works on all screen sizes
- 📋 All data in table format - easy to read and understand

## JSON Schema Format

The schema should be formatted as a JSON object that defines the fields you want to extract from the document. For example:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "VendorName": {
      "type": "string",
      "description": "Name of the vendor issuing the invoice"
    },
    "Vendor Address": {
      "type": "string",
      "description": "Full address of the vendor"
    },
    "Vendor Phone number": {
      "type": "string",
      "description": "Phone number"
    },
    "Billing Address": {
      "type": "string",
      "description": "Full name and address of the billing entity"
    },
    "Product Item List": {
      "type": "array",
      "items": {
        "type": "object",
        "description": "Table containing the list of products",
        "properties": {
          "Item ID": {
            "type": "string",
            "description": "Item id"
          },
          "Item Description": {
            "type": "string",
            "description": "Full description for the item"
          },
          "Quantity": {
            "type": "number",
            "description": "Number of items"
          },
          "Unit Price": {
            "type": "number"
          },
          "Line total": {
            "type": "number",
            "description": "Line total for the product line item"
          }
        }
      },
      "description": "Table containing the list of products"
    },
    "Total amount": {
      "type": "number"
    }
  }
}
```

## Authentication

The application uses OAuth 2.0 Web Server Flow (Authorization Code Grant) for authentication with Salesforce Data Cloud. The authentication flow:

1. **User clicks "Authenticate" button** - Frontend calls `/api/auth-info` to get Salesforce configuration
2. **User logs into Salesforce** - User enters credentials on Salesforce login page
3. **Salesforce redirects back** - With a code in the URL
4. **Token is exchanged and saved** - Backend exchanges the code for an access token and instance URL, which are stored in `access-token.secret`
5. **Token is used for API calls** - All subsequent API calls use the stored token and instance URL

### Token Management

- **Storage**: Access tokens and instance URLs are stored locally in `access-token.secret`
- **Security**: The token file is automatically added to `.gitignore` to prevent accidental commits
- **Expiration**: Salesforce access tokens expire. When expired, users will need to re-authenticate
- **Validation**: The application checks authentication status before allowing document processing

## Troubleshooting

### Common Issues

1. **Authentication Errors**: If you receive a 401 or 403 error, your access token may be expired. Click the "Authenticate" button to get a new token.
   
2. **Connected App Configuration**: Ensure your Salesforce Connected App has the correct callback URL and OAuth scopes configured.

3. **Schema Errors**: Ensure your schema is valid JSON and follows the expected format for the Salesforce Data Cloud Document AI API.

4. **File Format Issues**: Check that your document is in one of the supported formats and is not corrupted.

5. **Data Cloud Ingestion Failures**: Check the `_ingestion_status` field in the response. Common causes:
   - Invalid Data Cloud Connector Name or Object Name
   - Incorrect path format (should be `api/v1/ingest/sources/{connector}/{object}`)
   - Schema mismatch between extraction and Data Cloud
   - Missing Data Cloud permissions
   - Check server logs for detailed debug information
   - See [DATACLOUD_INGESTION.md](DATACLOUD_INGESTION.md) for detailed troubleshooting

### Debugging

The application has logging enabled. Check the console output for detailed error messages and debugging information.

## Security Considerations

This testbed is intended for development and testing purposes only. For production use:

1. Never hardcode authentication tokens in your code
2. Implement proper user authentication and authorization
3. Use HTTPS in production for secure token transmission
4. Consider implementing token refresh logic for long-running applications
5. Store tokens in secure, encrypted storage rather than local files

## API Endpoints

- `GET /` - Main application interface
- `GET /config` - Configuration page
- `GET /api/status` - Check authentication status
- `GET /api/auth-info` - Get OAuth configuration
- `GET /api/config` - Get current configuration
- `POST /api/config` - Save configuration
- `POST /api/config/reset` - Reset configuration to defaults
- `GET /api/schema` - Get current schema
- `GET /auth/callback` - OAuth callback page (handles code exchange)
- `POST /extract-data` - Process document extraction + Data Cloud ingestion

### Data Cloud Integration Flow
1. **Extract Data**: `/extract-data` processes document with AI
2. **Token Exchange**: Automatic Salesforce → Data Cloud token conversion
3. **Data Transformation**: Adds EventID (UUID) + eventime (timestamp)
4. **Ingestion**: POSTs data to Data Cloud streaming API
5. **Response**: Returns extracted data + ingestion status

## Dependencies

- Flask==3.0.2
- Werkzeug==3.0.1
- requests==2.31.0

## License

This project is licensed under the MIT License - see the LICENSE file for details.
