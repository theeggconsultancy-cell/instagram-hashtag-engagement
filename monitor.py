#!/usr/bin/env python3
"""
Instagram Hashtag Engagement Monitor - MVP

This script monitors Instagram hashtags and sends notifications about 
high-quality posts that might be worth engaging with manually.
"""

import time
import schedule
from typing import List, Dict
from datetime import datetime

from src.config import Config
from src.instagram_client import InstagramClient
from src.content_scorer import ContentScorer
from src.notifier import TelegramNotifier
from src.storage import StorageManager


class HashtagMonitor:
    """Main class for monitoring Instagram hashtags"""
    
    def __init__(self):
        self.instagram_client = InstagramClient()
        self.content_scorer = ContentScorer(Config.MIN_ENGAGEMENT_RATE)
        self.notifier = TelegramNotifier()
        self.storage = StorageManager()
        
    def run_check(self):
        """Run a single check cycle"""
        print(f"\n{'='*50}")
        print(f"🔍 Starting hashtag check at {datetime.now()}")
        print(f"{'='*50}")
        
        all_posts = []
        
        # Check each hashtag
        for hashtag in Config.HASHTAGS:
            print(f"\n📍 Checking hashtag: #{hashtag}")
            
            try:
                posts = self.instagram_client.search_hashtag(hashtag, Config.MAX_POSTS_PER_CHECK)
                print(f"   Found {len(posts)} posts")
                
                # Filter out already processed posts
                new_posts = []
                for post in posts:
                    if not self.storage.is_post_processed(post['id']):
                        new_posts.append(post)
                
                print(f"   {len(new_posts)} new posts (not previously processed)")
                all_posts.extend(new_posts)
                
            except Exception as e:
                print(f"   ❌ Error checking hashtag #{hashtag}: {e}")
                continue
        
        if not all_posts:
            print("\n💭 No new posts found across all hashtags")
            return
        
        # Score and filter posts
        print(f"\n📊 Scoring {len(all_posts)} total new posts...")
        filtered_posts = self.content_scorer.filter_posts(all_posts)
        
        print(f"   ✅ {len(filtered_posts)} posts passed quality filters")
        
        if not filtered_posts:
            print("   💭 No posts met the quality criteria")
            # Mark all posts as processed even if they didn't qualify
            post_ids = [post['id'] for post in all_posts]
            self.storage.mark_posts_processed(post_ids)
            return
        
        # Send notifications
        print(f"\n📱 Sending notifications for top posts...")
        try:
            if len(filtered_posts) == 1:
                # Send individual notification
                self.notifier.send_notification_sync(filtered_posts[0])
            else:
                # Send batch notification
                self.notifier.send_batch_sync(filtered_posts[:5])  # Top 5 posts
            
            print(f"   ✅ Notifications sent successfully")
            
        except Exception as e:
            print(f"   ❌ Error sending notifications: {e}")
        
        # Mark posts as processed
        post_ids = [post['id'] for post in all_posts]
        self.storage.mark_posts_processed(post_ids)
        
        # Save posts data for debugging
        self.storage.save_posts_data(filtered_posts, f"filtered_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        print(f"\n✅ Check cycle completed at {datetime.now()}")
        print(f"📊 Storage stats: {self.storage.get_stats()}")
    
    def start_scheduled_monitoring(self):
        """Start scheduled monitoring"""
        print("🚀 Starting Instagram Hashtag Monitor (Scheduled Mode)")
        print(f"📅 Check interval: every {Config.CHECK_INTERVAL_HOURS} hours")
        print(f"📍 Monitoring hashtags: {', '.join(Config.HASHTAGS)}")
        print(f"🎯 Min engagement rate: {Config.MIN_ENGAGEMENT_RATE}")
        print(f"📊 Max posts per check: {Config.MAX_POSTS_PER_CHECK}")
        
        # Schedule the job
        schedule.every(Config.CHECK_INTERVAL_HOURS).hours.do(self.run_check)
        
        # Run once immediately
        self.run_check()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute for scheduled jobs
    
    def run_once(self):
        """Run a single check (for testing)"""
        print("🧪 Running single hashtag check...")
        self.run_check()


def main():
    """Main entry point"""
    # Validate configuration
    errors = Config.validate()
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   • {error}")
        print("\nPlease check your .env file and fix the issues above.")
        return
    
    print("✅ Configuration validated successfully")
    
    monitor = HashtagMonitor()
    
    # For testing, run once
    # For production, use start_scheduled_monitoring()
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--schedule':
        monitor.start_scheduled_monitoring()
    else:
        monitor.run_once()


if __name__ == "__main__":
    main()