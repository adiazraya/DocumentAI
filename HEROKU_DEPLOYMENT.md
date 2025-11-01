# Heroku Deployment Guide

This guide will walk you through deploying the Document AI application to Heroku.

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com) (free tier available)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure git is installed on your machine

## Step 1: Verify Deployment Files

The following files have been created/updated for Heroku deployment:

### ✅ Procfile
Tells Heroku how to run your application:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT --timeout 180
```

### ✅ runtime.txt
Specifies Python version:
```
python-3.12.11
```

### ✅ requirements.txt
Includes all dependencies including `gunicorn` (Heroku's production server)

### ✅ .gitignore
Ensures sensitive files aren't committed to git

## Step 2: Prepare Your Git Repository

If not already initialized, initialize git in your project:

```bash
cd /path/to/DocumentAI
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

If already initialized, commit any pending changes:

```bash
git add .
git commit -m "Prepare for Heroku deployment"
```

## Step 3: Login to Heroku

```bash
heroku login
```

This will open a browser window for authentication.

## Step 4: Create Heroku App

```bash
heroku create your-app-name
```

Replace `your-app-name` with your desired app name (must be unique across Heroku). If you don't specify a name, Heroku will generate one for you.

**Example:**
```bash
heroku create salesforce-documentai-demo
```

Your app will be available at: `https://your-app-name.herokuapp.com`

**Note your Heroku URL** - you'll need it for the OAuth callback configuration!

## Step 5: Configure Environment Variables

Set your environment variables on Heroku (these replace your `.env` file):

```bash
heroku config:set LOGIN_URL=https://login.salesforce.com
heroku config:set CLIENT_ID=your_salesforce_client_id
heroku config:set CLIENT_SECRET=your_salesforce_client_secret
heroku config:set API_VERSION=v64.0
heroku config:set TOKEN_FILE=access-token.secret
heroku config:set FLASK_DEBUG=False
```

**Important**: Replace the values with your actual Salesforce Connected App credentials.

You can verify your config:
```bash
heroku config
```

## Step 6: Update Salesforce OAuth Callback URL

### 🔧 In Salesforce Setup:

1. Go to **Setup** → **Apps** → **App Manager**
2. Find your Connected App and click **Edit**
3. Scroll to **API (Enable OAuth Settings)**
4. In **Callback URL**, add your Heroku URL:

   ```
   https://your-app-name.herokuapp.com/auth/callback
   ```

   **Important**: 
   - Use `https://` (not `http://`)
   - Use your actual Heroku app name
   - Path must be `/auth/callback`

5. If you want to keep localhost for development, you can have multiple callback URLs:
   ```
   http://localhost:3000/auth/callback
   https://your-app-name.herokuapp.com/auth/callback
   ```

6. Click **Save**

### 📋 Example Callback URLs:

| Environment | Callback URL |
|-------------|--------------|
| Local Dev | `http://localhost:3000/auth/callback` |
| Heroku Production | `https://salesforce-documentai-demo.herokuapp.com/auth/callback` |

## Step 7: Deploy to Heroku

Push your code to Heroku:

```bash
git push heroku main
```

**Note**: If your branch is named `master` instead of `main`, use:
```bash
git push heroku master
```

## Step 8: Scale the Web Dyno

Ensure at least one web dyno is running:

```bash
heroku ps:scale web=1
```

## Step 9: Open Your App

```bash
heroku open
```

Or visit: `https://your-app-name.herokuapp.com`

## Step 10: Configure the Application

1. Visit your Heroku app URL
2. Click **⚙️ Configuration**
3. Enter your Salesforce credentials (they should auto-populate from Heroku config vars)
4. Configure ML Model: `llmgateway__VertexAIGemini20Flash001`
5. Configure Data Cloud:
   - Connector Name: `ContactIngestion`
   - Object Name: `LeadRecord`
6. Configure your JSON schema
7. Click **💾 Save Configuration**
8. Test authentication by clicking **Authenticate with Salesforce**

## Monitoring & Debugging

### View Logs
```bash
heroku logs --tail
```

This shows real-time logs including the detailed debug output for Data Cloud ingestion.

### Check App Status
```bash
heroku ps
```

### Restart App
```bash
heroku restart
```

### Access Heroku Dashboard
```bash
heroku dashboard
```

## Troubleshooting

### Issue: "Application Error"

**Check logs:**
```bash
heroku logs --tail
```

**Common causes:**
- Missing environment variables
- Incorrect Procfile
- Module import errors

### Issue: OAuth Redirect Mismatch

**Error:** "redirect_uri_mismatch"

**Solution:**
1. Verify the callback URL in Salesforce matches exactly: `https://your-app-name.herokuapp.com/auth/callback`
2. Clear browser cache and cookies
3. Try authentication again

### Issue: Port Binding Error

**Error:** "Error R10 (Boot timeout)"

**Solution:** Ensure `Procfile` uses `$PORT` variable (already configured)

### Issue: Data Cloud Ingestion Fails

**Check:**
1. View logs: `heroku logs --tail`
2. Look for "DATA CLOUD TOKEN EXCHANGE" and "DATA CLOUD INGESTION" debug output
3. Verify connector and object names in configuration

## Updating Your Deployment

After making code changes:

```bash
git add .
git commit -m "Your commit message"
git push heroku main
```

Heroku will automatically rebuild and redeploy.

## Environment Variables Management

### List all config vars:
```bash
heroku config
```

### Set a config var:
```bash
heroku config:set VARIABLE_NAME=value
```

### Remove a config var:
```bash
heroku config:unset VARIABLE_NAME
```

## Database & File Storage

**Important Notes:**

1. **Ephemeral Filesystem**: Heroku uses an ephemeral filesystem. Files like `access-token.secret` and `user_config.json` will be lost on dyno restart.

2. **Solution**: The app stores configuration in `user_config.json` which persists during the dyno's lifetime but will reset on restart. For production, consider:
   - Using Heroku Postgres for configuration storage
   - Using Heroku Redis for session/token storage
   - Re-authenticating on each session

3. **Current Behavior**: Users will need to:
   - Configure the app after first deployment
   - Re-authenticate with Salesforce if the dyno restarts
   - Configuration persists during active sessions

## Scaling (If Needed)

### Upgrade to Hobby Dyno ($7/month):
```bash
heroku dyno:type hobby
```

Benefits:
- App never sleeps
- SSL certificate included
- Better performance

### Scale to multiple dynos:
```bash
heroku ps:scale web=2
```

## Security Best Practices

1. ✅ **HTTPS**: Heroku provides free SSL/TLS
2. ✅ **Environment Variables**: Never commit secrets to git
3. ✅ **Secret Files**: `.gitignore` prevents committing `*.secret` files
4. ⚠️ **Consider**: Adding HTTP Basic Auth for production use
5. ⚠️ **Consider**: Restricting OAuth callback to specific domains in Salesforce

## Custom Domain (Optional)

If you want to use a custom domain:

```bash
heroku domains:add www.yourdomain.com
```

Then update your DNS records and Salesforce callback URL accordingly.

## Cost Estimate

- **Free Tier**: Free (with some limitations)
  - App sleeps after 30 minutes of inactivity
  - 550-1000 free dyno hours per month
  
- **Hobby**: $7/month
  - Never sleeps
  - Custom domain support
  
- **Production**: $25+/month
  - Multiple dynos
  - Better performance

## Next Steps

1. ✅ Deploy to Heroku
2. ✅ Update OAuth callback in Salesforce
3. ✅ Configure the application
4. ✅ Test document extraction
5. ✅ Monitor logs for any issues
6. 📊 Consider upgrading to Hobby dyno for production use
7. 🔒 Implement additional security measures if needed

## Support & Resources

- Heroku Dev Center: [devcenter.heroku.com](https://devcenter.heroku.com)
- Heroku Status: [status.heroku.com](https://status.heroku.com)
- Salesforce OAuth: [help.salesforce.com](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_web_server_flow.htm)

---

## Quick Reference Commands

```bash
# Deploy
git push heroku main

# View logs
heroku logs --tail

# Restart app
heroku restart

# Open app
heroku open

# Check status
heroku ps

# Set environment variable
heroku config:set VARIABLE=value

# Access bash shell
heroku run bash

# Check app info
heroku info
```

## Example: Complete First-Time Deployment

```bash
# 1. Login
heroku login

# 2. Create app
heroku create my-documentai-app

# 3. Set environment variables
heroku config:set LOGIN_URL=https://login.salesforce.com
heroku config:set CLIENT_ID=3MVG9s...
heroku config:set CLIENT_SECRET=ABC123...
heroku config:set API_VERSION=v64.0
heroku config:set TOKEN_FILE=access-token.secret
heroku config:set FLASK_DEBUG=False

# 4. Deploy
git push heroku main

# 5. Scale
heroku ps:scale web=1

# 6. Open
heroku open

# 7. Monitor
heroku logs --tail
```

Then update your Salesforce OAuth callback URL to:
```
https://my-documentai-app.herokuapp.com/auth/callback
```

🎉 Your app is now live on Heroku!

