# Multi-Org Configuration Guide

## Overview

The application now supports multiple Salesforce org configurations, allowing you to easily switch between different Salesforce environments (production, sandbox, dev, etc.) without having to manually update credentials each time.

## Key Features

### 1. **Multiple Org Support**
- Configure and store multiple Salesforce org credentials
- Each org has its own:
  - Login URL
  - Client ID and Client Secret
  - API Version
  - ML Model preference
  - Data Cloud configuration
  - Schema configuration
  - Authentication token (stored separately)

### 2. **Easy Org Switching**
- Switch between orgs with a single click
- Current org selection is saved in a cookie (persists for 30 days)
- No need to re-enter credentials when switching

### 3. **Org Management**
- Create new orgs
- Delete existing orgs
- Update org configurations
- Each org is identified by a unique name

## How to Use

### First Time Setup

1. **Access Configuration Page**
   - Click the "⚙️ Configuration" button from the home page
   - Or navigate to `/config`

2. **Create Your First Org** (if not already created)
   - The app automatically creates a "default" org from your `.env` file
   - Or click "➕ New Org" to create a new one
   - Enter a unique name (e.g., "production", "sandbox", "dev")
   - Only use letters, numbers, hyphens, and underscores

3. **Configure Org Settings**
   - Fill in the Salesforce credentials:
     - Login URL (e.g., `login.salesforce.com` or `test.salesforce.com`)
     - Client ID (Consumer Key from Connected App)
     - Client Secret (Consumer Secret from Connected App)
     - API Version (e.g., `v62.0`)
   - Configure ML Model and Data Cloud settings
   - Configure your extraction schema
   - Click "💾 Save Configuration"

4. **Authenticate**
   - After saving, click "🔐 Authenticate with Salesforce"
   - Complete the OAuth flow
   - You're now authenticated for this org!

### Working with Multiple Orgs

#### Creating a New Org

1. Go to Configuration page
2. Click "➕ New Org"
3. Enter a unique org name
4. Click "✓ Create"
5. The new org will be created with default settings
6. Configure its credentials and settings
7. Save and authenticate

#### Switching Between Orgs

1. Go to Configuration page
2. Select the desired org from the dropdown
3. Click "🔄 Switch"
4. The app will switch to that org's configuration
5. Authentication status will update automatically

**Note:** Each org maintains its own authentication token. If you switch to an org that hasn't been authenticated yet, you'll need to authenticate it first.

#### Deleting an Org

1. Go to Configuration page
2. Select the org you want to delete
3. Click "🗑️ Delete"
4. Confirm the deletion
5. The org and its authentication token will be permanently deleted

### Understanding the UI

#### Home Page
- **Org Display**: Shows the current org name (🏢 icon)
- **Auth Status**: Shows authentication status for current org
- **Authenticate Button**: Appears when not authenticated

#### Configuration Page
- **Org Selection Section**: Manage and switch between orgs
- **Authentication Section**: Shows auth status and authenticate button
- **Configuration Sections**: Configure settings for the current org

## File Structure

### Configuration Storage

All org configurations are stored in:
```
orgs_config.json
```

Structure:
```json
{
  "orgs": {
    "production": {
      "auth": {
        "login_url": "login.salesforce.com",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "api_version": "v62.0"
      },
      "ml_model": "llmgateway__VertexAIGemini20Flash001",
      "datacloud_connector_name": "ContactIngestion",
      "datacloud_object_name": "LeadRecord",
      "schema": { ... }
    },
    "sandbox": {
      ...
    }
  },
  "current_org": "production"
}
```

### Token Storage

Each org's authentication token is stored separately:
```
access-token-{org_name}.secret
```

Examples:
- `access-token-production.secret`
- `access-token-sandbox.secret`
- `access-token-dev.secret`

## API Endpoints

### Org Management

- `GET /api/orgs` - List all orgs
- `GET /api/orgs/<org_name>` - Get org configuration
- `POST /api/orgs/<org_name>` - Create or update org
- `DELETE /api/orgs/<org_name>` - Delete org
- `POST /api/orgs/switch/<org_name>` - Switch to org (sets cookie)

### Existing Endpoints (Now Org-Aware)

- `GET /api/status` - Returns auth status and current org
- `GET /api/auth-info` - Returns current org's auth config
- `POST /auth/exchange` - Uses current org's credentials
- `POST /extract-data` - Uses current org's config and token

## Technical Details

### Cookie Management

The current org selection is stored in a browser cookie:
- Cookie name: `current_org`
- Max age: 30 days
- Automatically set when switching orgs

### Org Selection Priority

When determining the current org, the system checks in this order:
1. Cookie value (from browser)
2. Stored current_org (from orgs_config.json)
3. First available org

### Backward Compatibility

The old `user_config.json` file is no longer used. On first run with the new system:
- A "default" org is created from your `.env` file
- Existing configuration is migrated automatically

## Best Practices

1. **Use Descriptive Names**: Name your orgs clearly (e.g., "production", "uat-sandbox", "dev-org")

2. **Keep Credentials Secure**: 
   - Never commit `orgs_config.json` to version control
   - Add it to `.gitignore`
   - Token files are also sensitive

3. **One Org at a Time**: 
   - The app works with one org at a time
   - Switch orgs when you need to work with a different environment

4. **Re-authenticate When Needed**: 
   - Tokens expire after a period
   - Re-authenticate if you see auth errors

5. **Backup Configurations**: 
   - Keep a backup of `orgs_config.json`
   - Document your org configurations

## Troubleshooting

### "No org configured" Error
- Go to Configuration page
- Create a new org or verify existing org has valid configuration

### Authentication Fails After Switching
- Each org needs its own authentication
- Click authenticate after switching to a new org

### Org Not Showing in Dropdown
- Refresh the Configuration page
- Check `orgs_config.json` exists and has valid JSON

### Lost Cookie/Session
- The app will use the stored current_org
- Or select an org and click "Switch" to set the cookie again

## Migration from Old System

If you were using the old single-org system:

1. Your existing configuration from `.env` will be used to create a "default" org
2. Your existing `access-token.secret` will need to be replaced by org-specific tokens
3. Re-authenticate after the migration to generate the new token file format

## Summary

The multi-org feature provides:
- ✅ Easy management of multiple Salesforce environments
- ✅ Quick switching between orgs
- ✅ Separate authentication for each org
- ✅ Per-org configuration for ML models, schemas, etc.
- ✅ Cookie-based persistence of current selection
- ✅ Clean, intuitive UI for org management

You can now efficiently work with multiple Salesforce orgs without the hassle of manual configuration changes!

