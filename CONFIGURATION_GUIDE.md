# Configuration Guide

## Overview

The Document AI application now includes a user-friendly configuration page where you can manage authentication settings and schema configuration without editing code or environment files.

## Accessing the Configuration Page

1. Start the application: `python app.py`
2. Open your browser to `http://localhost:3000`
3. Click the **⚙️ Configuration** button in the top-right corner of the home page
4. Or navigate directly to: `http://localhost:3000/config`

## Configuration Sections

### 🔐 Authentication Configuration

Configure your Salesforce Data Cloud connection settings:

- **Login URL**: Your Salesforce login domain (e.g., `login.salesforce.com` or your custom domain)
- **Client ID**: The Consumer Key from your Salesforce Connected App
- **Client Secret**: The Consumer Secret from your Salesforce Connected App
- **API Version**: Salesforce API version (default: `v62.0`)

**Note**: If you leave these fields empty, the application will try to load values from your `.env` file as a fallback.

### 🤖 ML Model Configuration

Select the AI model for document extraction:

- **Gemini 2.0 Flash** (`llmgateway__VertexAIGemini20Flash001`) - Fast and efficient, recommended for most use cases
- **OpenAI GPT-4o** (`llmgateway__OpenAIGPT4Omni_08_06`) - High accuracy, best for complex documents

The selected model will be used automatically for all document processing.

### 📋 Schema Configuration

Define the JSON schema for document data extraction:

- The schema uses JSON Schema format
- Default schema extracts event information and lead tables from documents
- You can customize the schema to match your specific document structure
- The schema supports Spanish language extraction by default

## How Configuration Works

### Priority System

The application uses the following priority for loading configuration:

1. **User Configuration** (`user_config.json`) - Created when you save settings via the configuration page
2. **Environment Variables** (`.env` file) - Fallback if user configuration is not available

### Saving Configuration

1. Fill in the authentication details
2. Select your preferred ML model
3. Modify the schema as needed
4. Click **💾 Save Configuration**
5. The settings are saved to `user_config.json` in the application directory
6. The application automatically reloads the configuration

### Resetting to Defaults

If you want to reset to the original configuration:

1. Click **🔄 Reset to Defaults**
2. This will reload:
   - Authentication settings from `.env`
   - Default ML model (Gemini 2.0 Flash)
   - Schema from `schema.json`

## Default Schema

The default schema extracts:

- **Evento**: Event name (usually in the top-left of the document)
- **LeadsTable**: Array of lead information including:
  - Firstname
  - Lastname
  - Email
  - Date (format: DD/MM/YYYY)
  - Company

All text extraction is configured for Spanish language.

## Tips

1. **Keep Backups**: Before making major schema changes, save a copy of your working schema
2. **Test Changes**: After modifying the schema or changing ML models, test with a sample document
3. **ML Model Selection**: Start with Gemini 2.0 Flash for faster processing, switch to GPT-4o if you need higher accuracy
4. **JSON Validation**: The configuration page validates your JSON schema before saving
5. **Security**: The `user_config.json` file is automatically added to `.gitignore` to prevent accidentally committing sensitive credentials

## Troubleshooting

### Configuration Not Saving

- Check that the application has write permissions in its directory
- Verify that your JSON schema is valid (the page will show an error if invalid)

### Authentication Still Failing

- Ensure your Salesforce Connected App is properly configured
- Verify that the Client ID and Client Secret are correct
- Check that the Login URL matches your Salesforce instance

### Schema Not Working

- Verify the JSON structure is valid
- Ensure the schema matches your document structure
- Check the browser console for any error messages during extraction

## Files Created

The configuration page creates/modifies these files:

- `user_config.json` - Stores your custom configuration (automatically ignored by git)

## Example Configuration

```json
{
  "auth": {
    "login_url": "login.salesforce.com",
    "client_id": "your_client_id_here",
    "client_secret": "your_client_secret_here",
    "api_version": "v62.0"
  },
  "ml_model": "llmgateway__VertexAIGemini20Flash001",
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "Evento": {
        "type": "string",
        "description": "Event name"
      },
      "LeadsTable": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "Firstname": { "type": "string" },
            "Lastname": { "type": "string" },
            "Email": { "type": "string" },
            "Date": { "type": "string" },
            "Company": { "type": "string" }
          }
        }
      }
    }
  }
}
```

## Need Help?

If you encounter any issues with the configuration:

1. Check the browser console for error messages
2. Review the application logs in the terminal
3. Reset to defaults and try again
4. Verify your Salesforce Connected App settings

