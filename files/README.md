# Instagram Hashtag Engagement - Human-in-the-Loop Workflow

A human-in-the-loop Instagram hashtag engagement workflow using n8n that surfaces high-quality posts for manual engagement with AI-drafted comment suggestions.

## 🎯 Project Goal

Surface a small, high-quality, daily set of Instagram posts from specific hashtags, then let a human quickly open each post and manually like/comment using pre-drafted, on-brand suggestions.

## 📋 What This Project Does

- **Discovers** relevant Instagram posts via hashtag searches using Meta's Graph API
- **Scores & filters** posts based on engagement, relevance, and freshness
- **Generates** AI-powered comment suggestions for each high-quality post
- **Delivers** curated posts to Telegram/Slack for quick human review
- **Tracks** engagement activities without any automation violations

## 🚫 What This Project Doesn't Do

- No auto-liking, auto-following, or auto-commenting
- No scraping or headless-browser automation
- No management of DMs, follows/unfollows, or stories
- No API policy violations

## 📊 Success Metrics

- 5–20 high-relevance posts daily (configurable)
- <2 min median human time per day for manual engagement
- Zero API policy violations; no action blocks

## 🛠 Tech Stack

- **n8n** - Workflow automation platform
- **Meta Graph API** - Instagram data access
- **OpenAI API** - Comment suggestion generation
- **Google Sheets** - Data storage and configuration
- **Telegram/Slack** - Human interface for engagement

## 📋 Prerequisites

- Instagram Business/Creator account linked to Facebook Page
- Meta App with IG Graph API access and long-lived token
- n8n Cloud or self-hosted instance
- OpenAI API access
- Google Sheets or database for storage
- Telegram bot or Slack app for notifications

## 🚀 Quick Start

1. **Review the specification**: See [Issue #1](https://github.com/theeggconsultancy-cell/instagram-hashtag-engagement/issues/1) for complete workflow details
2. **Set up prerequisites**: Configure Meta App, Instagram account, and API access
3. **Create storage**: Set up Google Sheets with required schemas
4. **Configure n8n**: Import workflow and configure credentials
5. **Test workflow**: Run with sandbox hashtags before going live

## 📁 Project Structure
