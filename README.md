# Instagram Hashtag Engagement Monitor - MVP

🎯 **Human-in-the-Loop Instagram Hashtag Engagement Workflow**

Automatically discover and get notifications about high-quality Instagram posts from specific hashtags worth engaging with manually. This MVP respects API limits and provides a foundation for building a complete engagement workflow.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup wizard
python setup.py

# 3. Try the demo (no credentials needed)
python demo.py

# 4. Run a test check
python monitor.py

# 5. Start scheduled monitoring
python monitor.py --schedule
```

## 📋 What This MVP Does

- ✅ **Discovers** Instagram posts with specific hashtags (your own posts for MVP)
- ✅ **Scores & filters** posts based on engagement, freshness, and content quality
- ✅ **Sends notifications** to Telegram with direct links for manual engagement
- ✅ **Respects API limits** with built-in rate limiting
- ✅ **Prevents duplicates** by tracking processed posts
- ✅ **Zero automation violations** - notifications only, manual engagement

## 🛠 Setup Requirements

You'll need to provide:
- **Instagram Access Token** (from Meta Developers)
- **Instagram User ID** 
- **Telegram Bot Token** (from @BotFather)
- **Telegram Chat ID** (from @userinfobot)

Run `python setup.py` for step-by-step setup instructions and credential testing.

## 📁 Project Structure

```
├── monitor.py          # Main monitoring script
├── setup.py           # Setup wizard with credential testing
├── demo.py            # Demo with mock data (no credentials needed)
├── requirements.txt   # Python dependencies
├── src/               # Core modules
│   ├── config.py      # Configuration management
│   ├── instagram_client.py  # Instagram API client
│   ├── content_scorer.py    # Post scoring and filtering
│   ├── notifier.py    # Telegram notifications
│   └── storage.py     # Data persistence
└── data/              # Storage for processed posts
```

## 🎬 Try the Demo

Experience the system without any setup:

```bash
python demo.py
```

This runs the complete workflow with mock Instagram data to show you exactly how the system works.

## ⚙️ Configuration

Edit `.env` file:

```env
# Instagram API
INSTAGRAM_ACCESS_TOKEN=your_token_here
INSTAGRAM_USER_ID=your_user_id_here

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token_here  
TELEGRAM_CHAT_ID=your_chat_id_here

# Monitoring Settings
HASHTAGS=python,webdev,programming,tech
CHECK_INTERVAL_HOURS=6
MAX_POSTS_PER_CHECK=10
MIN_ENGAGEMENT_RATE=0.02
```

## 🔄 How It Works

1. **Search** - Finds posts containing your specified hashtags
2. **Score** - Evaluates posts on engagement, freshness, caption quality, media type
3. **Filter** - Only high-quality posts above threshold are selected
4. **Notify** - Sends curated posts to Telegram with direct links
5. **Track** - Remembers processed posts to avoid duplicates

## 📊 MVP Limitations & Next Steps

### Current MVP Scope
- ✅ Searches your own Instagram posts (requires your posts to contain target hashtags)
- ✅ Basic engagement scoring and filtering
- ✅ Telegram notifications with post links
- ✅ Rate limiting and duplicate prevention

### Production Roadmap
- 🔄 **Instagram Hashtag Search API** - Discover any public posts (requires app review)
- 🔄 **Advanced Scoring** - Follower ratios, reach data, ML-based relevance
- 🔄 **Multiple Platforms** - Slack, Discord, Email notifications  
- 🔄 **AI Comment Suggestions** - OpenAI integration for engagement ideas
- 🔄 **Web Dashboard** - GUI for configuration and analytics
- 🔄 **Database Storage** - PostgreSQL/MongoDB for scalability

## 🆘 Getting Help

1. **Try the demo first**: `python demo.py`
2. **Run setup wizard**: `python setup.py` 
3. **Check the detailed setup guide**: See `files/docs/setup-guide.md`
4. **Review error messages** - the system provides detailed feedback

## 📝 Documentation

- [`README_MVP.md`](README_MVP.md) - Detailed technical documentation
- [`files/docs/setup-guide.md`](files/docs/setup-guide.md) - Complete setup guide
- [`files/config/workflow-config.json`](files/config/workflow-config.json) - Configuration reference

---

**Note**: This MVP focuses on the core notification workflow. For discovering other users' posts, you'll need Instagram's Hashtag Search API which requires additional permissions and app review from Meta.
