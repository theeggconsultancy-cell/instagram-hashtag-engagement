# Setup Guide - Instagram Hashtag Engagement Workflow

## Step 1: Meta App & Instagram API Setup

### Create Meta App
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create new app → Business → App name: "Hashtag Engagement Tool"
3. Add Instagram Basic Display product

### Get Instagram Access Token
1. App Dashboard → Instagram Basic Display → Basic Display
2. Create Instagram app
3. Add Instagram test user (your account)
4. Generate access token
5. Exchange for long-lived token (60 days)

### Required Permissions
- `instagram_graph_user_profile`
- `instagram_graph_user_media`
- `pages_read_engagement`

## Step 2: Google Sheets Setup

### Create Three Sheets

#### Sheet 1: hashtags_config