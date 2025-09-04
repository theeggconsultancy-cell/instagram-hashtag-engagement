# Instagram Hashtag Engagement Monitor - MVP

## Overview

This MVP provides automated monitoring of Instagram hashtags with push notifications for high-quality posts worth manual engagement. The system respects Instagram's API limits and provides a human-in-the-loop workflow.

## Features

- 🔍 **Hashtag Monitoring**: Automatically searches for posts with specified hashtags
- 📊 **Content Scoring**: Filters and scores posts based on engagement, freshness, and quality
- 📱 **Push Notifications**: Sends curated posts to Telegram for quick review
- ⚡ **Rate Limiting**: Built-in API rate limiting to respect Instagram's limits
- 💾 **Duplicate Prevention**: Tracks processed posts to avoid sending duplicates
- 🛡️ **API Compliance**: No automation violations - notifications only for manual engagement

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Instagram API Configuration
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
INSTAGRAM_USER_ID=your_instagram_user_id_here

# Telegram Bot Configuration  
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Monitoring Configuration
HASHTAGS=python,webdev,programming,tech,startup
CHECK_INTERVAL_HOURS=6
MAX_POSTS_PER_CHECK=10
MIN_ENGAGEMENT_RATE=0.02
```

### 3. Run the Monitor

**Test run (single check):**
```bash
python monitor.py
```

**Scheduled monitoring:**
```bash
python monitor.py --schedule
```

## Required Credentials & Setup

### Instagram Access Token

You need a long-lived Instagram access token with these permissions:
- `instagram_graph_user_profile`
- `instagram_graph_user_media`

**Setup Steps:**
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app (Business type)
3. Add "Instagram Basic Display" product
4. Create an Instagram App in the product settings
5. Add your Instagram account as a test user
6. Generate an access token and exchange for long-lived token (60 days)

### Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token
4. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `HASHTAGS` | Comma-separated list of hashtags to monitor | `python,webdev,programming` |
| `CHECK_INTERVAL_HOURS` | Hours between checks | `6` |
| `MAX_POSTS_PER_CHECK` | Maximum posts to analyze per hashtag | `10` |
| `MIN_ENGAGEMENT_RATE` | Minimum engagement rate for notifications | `0.02` |

## How It Works

1. **Discovery**: Searches Instagram for posts containing specified hashtags
2. **Scoring**: Evaluates posts based on:
   - Engagement rate (likes + comments)
   - Post freshness (newer posts score higher)
   - Caption quality (length, questions, spam detection)
   - Media type preference (video > carousel > image)
3. **Filtering**: Only posts above the minimum engagement threshold are considered
4. **Notification**: Sends top-scoring posts to Telegram with direct links
5. **Tracking**: Stores processed post IDs to prevent duplicate notifications

## Rate Limiting

The system automatically respects Instagram's API limits:
- Maximum 200 requests per hour
- Built-in request throttling
- Automatic waiting when limits are approached

## File Structure

```
├── monitor.py              # Main monitoring script
├── requirements.txt        # Python dependencies
├── .env.example           # Example configuration
├── src/
│   ├── config.py          # Configuration management
│   ├── instagram_client.py # Instagram API client
│   ├── content_scorer.py   # Post scoring logic
│   ├── notifier.py        # Telegram notifications
│   └── storage.py         # Data persistence
└── data/                  # Storage for processed posts and logs
```

## Important Notes

### MVP Limitations

1. **Hashtag Search**: Currently uses your own Instagram posts that contain hashtags. For production, you'd need Instagram Hashtag Search API access which requires additional permissions and app review.

2. **Engagement Calculation**: Uses simplified engagement metrics. Production would benefit from follower count and reach data.

3. **Storage**: Uses JSON files for simplicity. Consider upgrading to a database for production.

### Instagram API Limitations

- Long-lived tokens expire after 60 days and need renewal
- Hashtag Search API requires special permissions and app review
- Rate limits apply (200 requests/hour)

## Troubleshooting

### Common Issues

1. **"Configuration errors"**: Check your `.env` file has all required values
2. **"Error fetching Instagram media"**: Verify your access token and user ID
3. **"Failed to send Telegram notification"**: Check bot token and chat ID
4. **No posts found**: Ensure your Instagram posts contain the hashtags you're monitoring

### Getting Help

1. Check the error messages in the console output
2. Verify your credentials are correct
3. Test with a simple hashtag that you know exists in your posts
4. Check Instagram and Telegram API documentation for additional requirements

## Next Steps

This MVP can be extended with:
- Web dashboard for configuration and monitoring
- Database storage (PostgreSQL, MongoDB)
- Multiple notification channels (Slack, Discord, Email)
- Advanced hashtag discovery APIs
- AI-powered comment suggestions
- Engagement tracking and analytics