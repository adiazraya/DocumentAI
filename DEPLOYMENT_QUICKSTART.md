# 🚀 Quick Start: Deploy to Heroku

## Prerequisites
- Heroku account ([signup](https://signup.heroku.com/))
- Heroku CLI ([install](https://devcenter.heroku.com/articles/heroku-cli))
- Git installed

## Step 1: Login to Heroku
```bash
heroku login
```

## Step 2: Create Heroku App
```bash
heroku create your-app-name
```
Example: `heroku create salesforce-documentai`

**Note your app URL:** `https://your-app-name.herokuapp.com`

## Step 3: Set Environment Variables
```bash
heroku config:set LOGIN_URL=https://login.salesforce.com
heroku config:set CLIENT_ID=your_salesforce_client_id
heroku config:set CLIENT_SECRET=your_salesforce_client_secret
heroku config:set API_VERSION=v64.0
heroku config:set TOKEN_FILE=access-token.secret
heroku config:set FLASK_DEBUG=False
```

## Step 4: Update Salesforce OAuth Callback

1. Go to Salesforce **Setup** → **App Manager**
2. Find your Connected App → **Edit**
3. Update **Callback URL** to:
   ```
   https://your-app-name.herokuapp.com/auth/callback
   ```
4. **Save**

## Step 5: Deploy
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

## Step 6: Scale & Open
```bash
heroku ps:scale web=1
heroku open
```

## Step 7: Configure App
1. Click **⚙️ Configuration**
2. Enter your settings
3. **Save Configuration**
4. Test authentication

## Monitor Logs
```bash
heroku logs --tail
```

## Done! 🎉

Your app is live at: `https://your-app-name.herokuapp.com`

---

For detailed instructions, see:
- 📖 [HEROKU_DEPLOYMENT.md](HEROKU_DEPLOYMENT.md)
- 🔐 [SALESFORCE_OAUTH_SETUP.md](SALESFORCE_OAUTH_SETUP.md)

