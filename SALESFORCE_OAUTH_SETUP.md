# Salesforce OAuth Callback URL Configuration

This guide explains how to update the OAuth callback URL in your Salesforce Connected App for different deployment environments.

## Overview

The OAuth callback URL is where Salesforce redirects users after they authenticate. You need to update this URL when deploying to different environments.

## Callback URL Format

```
<protocol>://<domain><path>
```

**Path must always be:** `/auth/callback`

## Environment-Specific Callback URLs

| Environment | Callback URL |
|-------------|--------------|
| **Local Development** | `http://localhost:3000/auth/callback` |
| **Heroku** | `https://your-app-name.herokuapp.com/auth/callback` |
| **Custom Domain** | `https://yourdomain.com/auth/callback` |

**Important**: 
- Use `https://` for production (Heroku)
- Use `http://` only for localhost
- Path must be exactly `/auth/callback`

## Step-by-Step: Update Callback URL in Salesforce

### 1. Access Salesforce Setup

1. Log in to your Salesforce org
2. Click the **⚙️ gear icon** (top right)
3. Select **Setup**

### 2. Navigate to Connected Apps

**Method A: Quick Find**
1. In the Quick Find box (left sidebar), type: `App Manager`
2. Click **App Manager**

**Method B: Menu Navigation**
1. Navigate to: **Platform Tools** → **Apps** → **App Manager**

### 3. Find Your Connected App

1. In the App Manager list, find your Connected App
   - Look for the name you used when creating the Connected App
   - Example: "Document AI Integration"
2. Click the dropdown arrow (▼) on the right
3. Select **Edit** (or **Manage**)

### 4. Edit OAuth Settings

1. Scroll down to **API (Enable OAuth Settings)** section
2. Find **Callback URL** field
3. Update or add your new callback URL

#### For Heroku Deployment:

**Replace:**
```
http://localhost:3000/auth/callback
```

**With:**
```
https://your-app-name.herokuapp.com/auth/callback
```

Example:
```
https://salesforce-documentai.herokuapp.com/auth/callback
```

#### For Multiple Environments:

You can have **multiple callback URLs** (one per line):

```
http://localhost:3000/auth/callback
https://your-app-name.herokuapp.com/auth/callback
https://staging-app-name.herokuapp.com/auth/callback
```

This allows you to test locally and use production simultaneously.

### 5. Save Changes

1. Scroll down
2. Click **Save**
3. Salesforce may ask you to confirm - click **Continue** or **Save** again

### 6. Wait for Propagation (if needed)

Changes are usually immediate, but can take a few minutes to propagate across Salesforce servers. If you get redirect errors, wait 2-3 minutes and try again.

## Visual Guide

### Finding Your Connected App

```
Setup → Quick Find → "App Manager" → Your App → Edit
```

### OAuth Settings Section

Look for this section in your Connected App:

```
┌─────────────────────────────────────────────┐
│ API (Enable OAuth Settings)                 │
├─────────────────────────────────────────────┤
│ ☑ Enable OAuth Settings                     │
│                                              │
│ Callback URL:                                │
│ ┌─────────────────────────────────────────┐ │
│ │ https://your-app.herokuapp.com/auth/... │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ Selected OAuth Scopes:                       │
│ • Access and manage your data (api)          │
│ • Perform requests on your behalf at any... │
│ • Full access (full)                         │
└─────────────────────────────────────────────┘
```

## Common Errors and Solutions

### Error: "redirect_uri_mismatch"

**Full Error:**
```
error=redirect_uri_mismatch&error_description=redirect_uri%20must%20match%20configuration
```

**Causes:**
1. Callback URL in Salesforce doesn't match the actual redirect URL
2. Typo in the URL
3. Wrong protocol (http vs https)
4. Missing or extra slash

**Solutions:**
1. Verify exact URL match:
   - Salesforce: `https://your-app.herokuapp.com/auth/callback`
   - App URL: `https://your-app.herokuapp.com`
2. Check for typos
3. Use `https://` (not `http://`) for Heroku
4. No trailing slash after `/callback`

### Error: "invalid_client_id"

**Causes:**
1. Wrong CLIENT_ID in environment variables
2. Connected App not yet approved/active

**Solutions:**
1. Verify CLIENT_ID in Heroku config: `heroku config:get CLIENT_ID`
2. Check Consumer Key in Salesforce matches
3. Ensure Connected App is approved (for production orgs)

### Error: OAuth Page Not Loading

**Causes:**
1. LOGIN_URL incorrect in environment variables
2. Network/firewall issues

**Solutions:**
1. Verify LOGIN_URL:
   - Production: `https://login.salesforce.com`
   - Sandbox: `https://test.salesforce.com`
   - Custom Domain: `https://yourdomain.my.salesforce.com`
2. Check Heroku config: `heroku config:get LOGIN_URL`

## Get Your Heroku App URL

If you don't know your Heroku app URL:

```bash
heroku info
```

Look for the **Web URL** line:
```
Web URL:       https://your-app-name.herokuapp.com
```

Or simply:
```bash
heroku open
```

This opens your app and shows you the URL.

## Testing the Callback URL

### 1. Test Locally (Development)

**Callback URL:** `http://localhost:3000/auth/callback`

1. Start your app: `python app.py`
2. Visit: `http://localhost:3000`
3. Click **Authenticate with Salesforce**
4. Should redirect to Salesforce login
5. After login, should redirect back to: `http://localhost:3000/auth/callback`
6. Then redirect to: `http://localhost:3000/config`

### 2. Test on Heroku (Production)

**Callback URL:** `https://your-app.herokuapp.com/auth/callback`

1. Visit: `https://your-app.herokuapp.com`
2. Click **⚙️ Configuration**
3. Click **Authenticate with Salesforce**
4. Should redirect to Salesforce login
5. After login, should redirect back to: `https://your-app.herokuapp.com/auth/callback`
6. Then redirect to: `https://your-app.herokuapp.com/config`

## OAuth Scopes

Ensure your Connected App has these OAuth scopes:

### Required Scopes:

- ✅ **Access and manage your data (api)**
- ✅ **Perform requests on your behalf at any time (refresh_token, offline_access)**
- ✅ **Access unique user identifiers (openid)**

### Optional (for Data Cloud):

- ☑️ **Full access (full)** - If you need broader access
- ☑️ **Access Data Cloud resources** - If available in your org

### How to Check/Update Scopes:

1. In Connected App settings
2. Scroll to **Selected OAuth Scopes**
3. Move required scopes from **Available** to **Selected**
4. Click **Save**

## Security Best Practices

### 1. Use HTTPS in Production
❌ `http://your-app.herokuapp.com/auth/callback`  
✅ `https://your-app.herokuapp.com/auth/callback`

### 2. Restrict OAuth Scope
Only enable the scopes your app actually needs.

### 3. IP Restrictions (Optional)
For production, consider adding IP restrictions in Salesforce:
1. Connected App settings
2. **IP Relaxation**: Enforce IP restrictions
3. Add allowed IP ranges

### 4. Session Security
Set appropriate session timeout in Salesforce and your app.

## Multiple Environments Setup

If you have multiple environments:

### Development
```
http://localhost:3000/auth/callback
```

### Staging
```
https://staging-documentai.herokuapp.com/auth/callback
```

### Production
```
https://documentai.herokuapp.com/auth/callback
```

Add all three to your Connected App callback URLs (one per line).

## Checklist: Heroku Deployment

Before deploying to Heroku, ensure:

- [ ] Heroku app is created
- [ ] Heroku app URL is noted: `https://______.herokuapp.com`
- [ ] Salesforce Connected App callback URL is updated
- [ ] Environment variables are set on Heroku
- [ ] `Procfile` exists in project root
- [ ] `runtime.txt` exists in project root
- [ ] `gunicorn` is in `requirements.txt`
- [ ] Code is committed to git
- [ ] OAuth callback test passes

## Quick Reference

### Get Your Connected App Details

**Consumer Key (CLIENT_ID):**
1. Setup → App Manager → Your App → View
2. Copy "Consumer Key"

**Consumer Secret (CLIENT_SECRET):**
1. Click "Click to reveal" next to Consumer Secret
2. Copy the secret
3. **Keep this secret!** Don't share or commit to git

**Callback URL to Set:**
```
https://your-heroku-app-name.herokuapp.com/auth/callback
```

### Environment Variables to Set on Heroku

```bash
heroku config:set LOGIN_URL=https://login.salesforce.com
heroku config:set CLIENT_ID=<your_consumer_key>
heroku config:set CLIENT_SECRET=<your_consumer_secret>
heroku config:set API_VERSION=v64.0
```

## Need Help?

### Check Logs
```bash
# Heroku logs
heroku logs --tail

# Look for OAuth errors
heroku logs --tail | grep -i oauth
```

### Test OAuth Flow
```bash
# Open your app
heroku open

# Watch logs while testing authentication
heroku logs --tail
```

### Salesforce Setup Errors
- Check "Setup Audit Trail" in Salesforce for recent changes
- Verify Connected App is "Active"
- Check if profile/permission set has access to the Connected App

## Resources

- [Salesforce OAuth 2.0 Web Server Flow](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm)
- [Connected Apps Setup](https://help.salesforce.com/s/articleView?id=sf.connected_app_create.htm)
- [Heroku Python Deployment](https://devcenter.heroku.com/articles/getting-started-with-python)

---

**Last Updated:** November 2025  
**App Version:** 2.0 with Data Cloud Integration

