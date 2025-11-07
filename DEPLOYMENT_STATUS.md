# 🎉 Heroku Deployment - Complete!

## Deployment Information

✅ **Status**: Successfully Deployed  
🌐 **App URL**: https://wt25-document-ai-026b38fac7d8.herokuapp.com/  
📦 **Heroku App Name**: wt25-document-ai  
🐍 **Python Version**: 3.12.12 (latest)  
📅 **Deployed**: November 7, 2025  
🆕 **Version**: v19 (with multi-org support)

## What's New - Multi-Org Support

Your app now supports **multiple Salesforce org configurations**! Features include:

✨ **Multiple Org Management**
- Configure unlimited Salesforce orgs (production, sandbox, dev, etc.)
- Each org has separate credentials, settings, and authentication
- Switch between orgs with a single click
- Cookie-based org selection (persists for 30 days)

🎯 **Per-Org Configuration**
- Separate authentication tokens for each org
- Independent ML model selection per org
- Unique Data Cloud settings per org
- Custom extraction schemas per org

## Next Steps - Configure Your App

### 1. Access Your App

Visit: https://wt25-document-ai-026b38fac7d8.herokuapp.com/

### 2. Create Your First Org

1. Click **⚙️ Configuration**
2. You'll see the "default" org (created from your environment variables)
3. Or create a new org:
   - Click **➕ New Org**
   - Enter a name (e.g., "production", "sandbox")
   - Click **✓ Create**

### 3. Configure Org Credentials

For each org, configure:

**Authentication Settings:**
- Login URL: `login.salesforce.com` or `test.salesforce.com`
- Client ID: Your Connected App's Consumer Key
- Client Secret: Your Connected App's Consumer Secret
- API Version: `v62.0` (or your preferred version)

**ML Model:**
- Select: `llmgateway__VertexAIGemini20Flash001` or `llmgateway__OpenAIGPT4Omni_08_06`

**Data Cloud Settings:**
- Connector Name: Your Data Cloud connector (e.g., `ContactIngestion`)
- Object Name: Your Data Cloud object (e.g., `LeadRecord`)

**Schema:**
- Configure your JSON extraction schema
- Or use the JSON Schema Generator tool

Click **💾 Save Configuration**

### 4. Update Salesforce OAuth Callback

⚠️ **IMPORTANT**: Update your Connected App in Salesforce:

1. Go to Salesforce Setup → Apps → App Manager
2. Find your Connected App → Edit
3. Under OAuth Settings, add/update Callback URL:
   ```
   https://wt25-document-ai-026b38fac7d8.herokuapp.com/auth/callback
   ```
4. You can keep multiple callback URLs (for local dev):
   ```
   http://localhost:3000/auth/callback
   https://wt25-document-ai-026b38fac7d8.herokuapp.com/auth/callback
   ```
5. Save

### 5. Authenticate Each Org

After configuring an org:
1. Stay on the Configuration page
2. Click **🔐 Authenticate with Salesforce**
3. Complete the OAuth flow
4. You're authenticated! ✓

### 6. Test Document Processing

1. Return to the home page
2. You'll see your current org displayed (🏢 icon)
3. Upload or capture a document
4. Click **Analyze Document**
5. View extracted data and Data Cloud ingestion results

## Switching Between Orgs

### From Configuration Page:
1. Select org from dropdown
2. Click **🔄 Switch**
3. Configure and authenticate if needed

### From Home Page:
- Current org is displayed in the header
- Authentication status shown per org
- To switch, go to Configuration page

## Important Notes About Heroku

### ⚠️ Ephemeral Filesystem

Heroku uses an ephemeral filesystem. This means:

**What Gets Lost on Dyno Restart:**
- All org configurations (`orgs_config.json`)
- All authentication tokens (`access-token-*.secret`)
- Typically happens every 24 hours or when you deploy

**What This Means:**
- After a restart, you'll need to reconfigure your orgs
- You'll need to re-authenticate each org
- Configuration persists during active sessions

**Solutions for Production:**
1. **Accept Re-configuration**: OK for demos/testing
2. **Upgrade to Hobby Dyno**: More stable ($7/month)
3. **Add Database**: Store configs in Heroku Postgres (requires code changes)
4. **Use Redis**: Store configs in Heroku Redis (requires code changes)

### Current Dyno Status

```bash
# Check status
heroku ps

# View logs
heroku logs --tail

# Restart if needed
heroku restart
```

## Managing Your Deployment

### View Real-Time Logs

```bash
heroku logs --tail
```

Look for:
- Authentication status
- API calls
- Data Cloud token exchange
- Data Cloud ingestion results
- Any errors

### Update Configuration

To change environment variables:

```bash
heroku config:set VARIABLE_NAME=value
```

View all config vars:

```bash
heroku config
```

### Deploy Updates

After making code changes:

```bash
git add .
git commit -m "Your commit message"
git push heroku main
```

### Open App

```bash
heroku open
```

## Monitoring & Troubleshooting

### Check App Status

```bash
heroku ps
```

Should show:
```
web.1: up [date] (~ Xm ago)
```

### Common Issues

**Issue: "Application Error"**
- Run: `heroku logs --tail`
- Check for errors
- Verify config vars are set

**Issue: OAuth Redirect Mismatch**
- Verify callback URL in Salesforce matches exactly
- Must be: `https://wt25-document-ai-026b38fac7d8.herokuapp.com/auth/callback`

**Issue: No Orgs Configured**
- Normal after dyno restart
- Go to Configuration → Create new org
- Configure and authenticate

**Issue: Token Expired**
- Click re-authenticate for that org
- Complete OAuth flow again

### Debug Mode

Logs are verbose and include:
- Request details
- Token exchange debugging
- Data Cloud API calls
- Ingestion responses

## Performance & Scaling

### Current Plan
- **Dyno Type**: Basic
- **Monthly Cost**: Check `heroku ps` output
- **Uptime**: May sleep after inactivity (Free tier)

### Upgrade Options

**To prevent sleeping ($7/month):**
```bash
heroku dyno:type hobby
```

**To scale up:**
```bash
heroku ps:scale web=2
```

## Testing Checklist

✅ App accessible at URL  
✅ Configuration page loads  
✅ Can create new org  
✅ Can configure org settings  
✅ Can save configuration  
✅ OAuth callback works  
✅ Can authenticate with Salesforce  
✅ Can upload document  
✅ Document extraction works  
✅ Data Cloud ingestion succeeds  
✅ Can switch between orgs  

## Useful Commands Reference

```bash
# View app info
heroku info

# Open app in browser
heroku open

# View logs
heroku logs --tail

# Restart app
heroku restart

# Check dyno status
heroku ps

# Set config variable
heroku config:set VAR=value

# View all config
heroku config

# Access bash shell
heroku run bash

# Check releases
heroku releases

# Rollback to previous version
heroku rollback v18
```

## Documentation

📖 **Multi-Org Guide**: See `MULTI_ORG_GUIDE.md` for detailed multi-org documentation  
📖 **Deployment Guide**: See `HEROKU_DEPLOYMENT.md` for complete deployment instructions  
📖 **Configuration Guide**: See `CONFIGURATION_GUIDE.md` for configuration details  

## Support Resources

- **Heroku Status**: https://status.heroku.com/
- **Heroku Dev Center**: https://devcenter.heroku.com/
- **Salesforce OAuth**: https://help.salesforce.com/
- **App Logs**: `heroku logs --tail`

## Security Reminders

✅ HTTPS enabled (automatic with Heroku)  
✅ Secrets not in git (`.gitignore` configured)  
✅ Environment variables used for sensitive data  
⚠️ Consider adding authentication for production use  
⚠️ Review Salesforce OAuth scope restrictions  

---

## Summary

🎉 **Your multi-org Document AI app is live and running!**

**App URL**: https://wt25-document-ai-026b38fac7d8.herokuapp.com/

Next: Visit your app, configure your orgs, and start processing documents!

**Need Help?**
- Check logs: `heroku logs --tail`
- Review documentation in this repo
- Check Heroku dashboard: `heroku dashboard`

Happy document processing! 🚀

