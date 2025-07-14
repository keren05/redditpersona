# Reddit User Persona Generator 

A Python script that analyzes Reddit profiles and generates AI-powered user personas from their posts and comments.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- [Reddit Developer Account](https://www.reddit.com/prefs/apps)
- [OpenAI API Key](https://platform.openai.com/api-keys)

### 2. Installation
-bash
git clone https://github.com/keren05/redditpersona.git
cd redditpersona
pip install -r requirements.txt

### 3. How to Get Reddit Client ID & Secret:

1. **Go to Reddit App Preferences**  
   Visit: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)  
   *(Log in to your Reddit account first)*

2. **Create New Application**  
   - Scroll down and click **"Create App"** or **"Create Another App"**  
   - Fill in the form:
     - **Name:** `Persona Generator` (or any name)
     - **App Type:** Select **"Script"**
     - **Description:** Optional (e.g., "For user persona analysis")
     - **Redirect URI:** `http://localhost:8080` (required but unused)

3. **Save Your Credentials**  
   After creation, you'll see:
   - 🔑 **Client ID** (14-character string under the app name)  
     Example: `p0w3rUs3rN4m3` → This is your `REDDIT_CLIENT_ID`
   - 🔒 **Client Secret** (30-character string)  
     Example: `xXx_Y0uRS3cr3tK3Y_xXx` → This is your `REDDIT_CLIENT_SECRET`

   ⚠️ **Important:**  
   - The secret is **only shown once** - save it immediately!  
   - If lost, generate a new one via **"Edit App"** → **"Regenerate Secret"**

---

## 4.  CREATE .env file
ADD credentials:
   ```ini
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
```
## 5. Run the script:

```bash
python redditpersona.py
```

## Troubleshooting
Error                                	  Solution
prawcore.exceptions.ResponseException- Check Reddit API keys
openai.AuthenticationError	         - Verify OpenAI key
Rate Limit Exceeded	                 - Wait 1-2 minutes
Profile Not Found	                   - User may be private/deleted




## License
For educational/personal use only. Reddit data ownership applies.

