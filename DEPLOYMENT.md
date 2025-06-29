# Deploying Story Weaver Bot to Render

## Prerequisites
- A GitHub account
- Your Google Gemini API key
- Your Unsplash API key

## Step-by-Step Deployment Guide

### 1. Prepare Your Repository
Make sure your code is pushed to a GitHub repository.

### 2. Create a Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email address

### 3. Deploy Your App
1. **Click "New +"** in your Render dashboard
2. **Select "Web Service"**
3. **Connect your GitHub repository**
4. **Configure your service:**
   - **Name:** `story-weaver-bot` (or any name you prefer)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

### 4. Set Environment Variables
In your Render service settings, add these environment variables:
- `GOOGLE_API_KEY` = Your Google Gemini API key
- `UNSPLASH_ACCESS_KEY` = Your Unsplash API key

### 5. Deploy
Click "Create Web Service" and wait for the deployment to complete.

### 6. Access Your App
Your app will be available at: `https://your-app-name.onrender.com`

## Troubleshooting

### Common Issues:
1. **Build fails:** Check that all dependencies are in `requirements.txt`
2. **App crashes:** Check the logs in Render dashboard
3. **API errors:** Verify your environment variables are set correctly

### Checking Logs:
1. Go to your service in Render dashboard
2. Click on "Logs" tab
3. Look for any error messages

## Free Tier Limitations
- Your app will sleep after 15 minutes of inactivity
- It will wake up when someone visits (may take 30-60 seconds)
- 750 hours of runtime per month
- 512 MB RAM

## Updating Your App
Simply push changes to your GitHub repository, and Render will automatically redeploy your app.

## Support
If you encounter issues, check Render's documentation or contact their support team. 