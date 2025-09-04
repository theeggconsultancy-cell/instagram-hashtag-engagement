#!/usr/bin/env python3
"""
Setup script for Instagram Hashtag Engagement Monitor

This script helps users set up their credentials and test the configuration.
"""

import os
import sys
import requests
from src.config import Config

def print_header():
    print("🔧 Instagram Hashtag Engagement Monitor - Setup")
    print("=" * 50)

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("📁 No .env file found. Let's create one...")
        
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("📝 Please edit .env file with your credentials")
            return False
        else:
            print("❌ No .env.example file found")
            return False
    else:
        print("✅ Found .env file")
        return True

def validate_instagram_token():
    """Test Instagram access token"""
    if not Config.INSTAGRAM_ACCESS_TOKEN:
        print("❌ Instagram access token not configured")
        return False
    
    if not Config.INSTAGRAM_USER_ID:
        print("❌ Instagram user ID not configured")
        return False
    
    print("🔍 Testing Instagram access token...")
    
    try:
        url = f"https://graph.instagram.com/{Config.INSTAGRAM_USER_ID}"
        params = {
            'fields': 'id,username',
            'access_token': Config.INSTAGRAM_ACCESS_TOKEN
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            username = data.get('username', 'Unknown')
            print(f"✅ Instagram token valid for user: @{username}")
            return True
        else:
            print(f"❌ Instagram API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Instagram token: {e}")
        return False

def validate_telegram_bot():
    """Test Telegram bot token"""
    if not Config.TELEGRAM_BOT_TOKEN:
        print("❌ Telegram bot token not configured")
        return False
    
    if not Config.TELEGRAM_CHAT_ID:
        print("❌ Telegram chat ID not configured")
        return False
    
    print("🔍 Testing Telegram bot...")
    
    try:
        # Test bot token
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_name = data.get('result', {}).get('first_name', 'Unknown')
                print(f"✅ Telegram bot token valid for bot: {bot_name}")
                
                # Test sending a message
                message_url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
                message_data = {
                    'chat_id': Config.TELEGRAM_CHAT_ID,
                    'text': '🧪 Test message from Instagram Hashtag Monitor setup'
                }
                
                message_response = requests.post(message_url, data=message_data)
                
                if message_response.status_code == 200:
                    print("✅ Test message sent successfully to Telegram")
                    return True
                else:
                    print(f"❌ Failed to send test message: {message_response.status_code}")
                    print(f"   Response: {message_response.text}")
                    return False
            else:
                print(f"❌ Telegram bot API error: {data}")
                return False
        else:
            print(f"❌ Telegram API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Telegram bot: {e}")
        return False

def print_instructions():
    """Print setup instructions"""
    print("\n📋 SETUP INSTRUCTIONS")
    print("=" * 30)
    
    print("\n🔐 Instagram Access Token:")
    print("1. Go to https://developers.facebook.com/")
    print("2. Create a new app (Business type)")
    print("3. Add 'Instagram Basic Display' product")
    print("4. Create Instagram app in product settings")
    print("5. Add your Instagram account as test user")
    print("6. Generate access token and exchange for long-lived token")
    print("7. Get your Instagram User ID")
    
    print("\n🤖 Telegram Bot Setup:")
    print("1. Message @BotFather on Telegram")
    print("2. Create new bot with /newbot")
    print("3. Get bot token from BotFather")
    print("4. Message @userinfobot to get your chat ID")
    print("5. Or start a chat with your bot and check logs")
    
    print("\n📝 Configuration:")
    print("Edit the .env file with your credentials:")
    print("- INSTAGRAM_ACCESS_TOKEN=your_token_here")
    print("- INSTAGRAM_USER_ID=your_user_id_here") 
    print("- TELEGRAM_BOT_TOKEN=your_bot_token_here")
    print("- TELEGRAM_CHAT_ID=your_chat_id_here")

def main():
    print_header()
    
    # Check for .env file
    if not check_env_file():
        print_instructions()
        return
    
    # Load configuration
    from dotenv import load_dotenv
    load_dotenv()
    
    print(f"\n📊 Current Configuration:")
    print(f"   Instagram Token: {'✅ Set' if Config.INSTAGRAM_ACCESS_TOKEN else '❌ Missing'}")
    print(f"   Instagram User ID: {'✅ Set' if Config.INSTAGRAM_USER_ID else '❌ Missing'}")
    print(f"   Telegram Bot Token: {'✅ Set' if Config.TELEGRAM_BOT_TOKEN else '❌ Missing'}")
    print(f"   Telegram Chat ID: {'✅ Set' if Config.TELEGRAM_CHAT_ID else '❌ Missing'}")
    print(f"   Hashtags: {', '.join(Config.HASHTAGS)}")
    print(f"   Check Interval: {Config.CHECK_INTERVAL_HOURS} hours")
    
    # Validate configuration
    errors = Config.validate()
    if errors:
        print(f"\n❌ Configuration errors found:")
        for error in errors:
            print(f"   • {error}")
        print("\nPlease fix these errors and run setup again.")
        print_instructions()
        return
    
    print(f"\n🧪 Testing Configuration...")
    print("-" * 30)
    
    # Test Instagram
    instagram_ok = validate_instagram_token()
    
    # Test Telegram
    telegram_ok = validate_telegram_bot()
    
    # Summary
    print(f"\n📋 Setup Summary:")
    print("-" * 20)
    print(f"Instagram API: {'✅ Working' if instagram_ok else '❌ Failed'}")
    print(f"Telegram Bot: {'✅ Working' if telegram_ok else '❌ Failed'}")
    
    if instagram_ok and telegram_ok:
        print(f"\n🎉 Setup completed successfully!")
        print(f"You can now run the monitor with:")
        print(f"   python monitor.py           # Single test run")
        print(f"   python monitor.py --schedule # Scheduled monitoring")
    else:
        print(f"\n❌ Setup incomplete. Please fix the issues above.")
        if not instagram_ok or not telegram_ok:
            print_instructions()

if __name__ == "__main__":
    main()