import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration management for Instagram Hashtag Engagement"""
    
    # Instagram API Configuration
    INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    INSTAGRAM_USER_ID = os.getenv('INSTAGRAM_USER_ID')
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    
    # Monitoring Configuration
    HASHTAGS = os.getenv('HASHTAGS', 'python,webdev,programming').split(',')
    CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', '6'))
    MAX_POSTS_PER_CHECK = int(os.getenv('MAX_POSTS_PER_CHECK', '10'))
    MIN_ENGAGEMENT_RATE = float(os.getenv('MIN_ENGAGEMENT_RATE', '0.02'))
    
    # API Rate Limiting
    INSTAGRAM_API_RATE_LIMIT = 200  # requests per hour
    RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
    
    # Storage
    DATA_DIR = 'data'
    PROCESSED_POSTS_FILE = os.path.join(DATA_DIR, 'processed_posts.json')
    
    @classmethod
    def validate(cls) -> List[str]:
        """Validate required configuration"""
        errors = []
        
        if not cls.INSTAGRAM_ACCESS_TOKEN:
            errors.append("INSTAGRAM_ACCESS_TOKEN is required")
        
        if not cls.INSTAGRAM_USER_ID:
            errors.append("INSTAGRAM_USER_ID is required")
            
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required")
            
        if not cls.TELEGRAM_CHAT_ID:
            errors.append("TELEGRAM_CHAT_ID is required")
            
        return errors