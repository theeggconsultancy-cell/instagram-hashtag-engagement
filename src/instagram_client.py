import requests
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
import os
from .config import Config

class InstagramClient:
    """Instagram Graph API Client with rate limiting"""
    
    def __init__(self):
        self.access_token = Config.INSTAGRAM_ACCESS_TOKEN
        self.user_id = Config.INSTAGRAM_USER_ID
        self.base_url = "https://graph.instagram.com"
        self.rate_limiter = RateLimiter(Config.INSTAGRAM_API_RATE_LIMIT, Config.RATE_LIMIT_WINDOW)
        
    def search_hashtag(self, hashtag: str, limit: int = 25) -> List[Dict]:
        """
        Search for recent posts with a specific hashtag
        Note: This MVP version searches your own posts. For production hashtag discovery,
        you'll need Instagram Hashtag Search API access which requires app review.
        """
        # For MVP, we'll use the user's own media and filter by hashtags
        # In production, you'd need Instagram Hashtag Search API access
        posts = self.get_user_media_with_hashtag(hashtag, limit)
        
        # Add a note to help users understand the limitation
        if posts:
            print(f"   📝 Note: Found {len(posts)} of your own posts with #{hashtag}")
            print(f"   🔄 For discovering other users' posts, you'll need Instagram Hashtag Search API")
        else:
            print(f"   💭 No posts found with #{hashtag} in your account")
            print(f"   💡 Try adding some posts with #{hashtag} to test the system")
        
        return posts
    
    def get_user_media_with_hashtag(self, hashtag: str, limit: int = 25) -> List[Dict]:
        """Get user's media posts that contain the specified hashtag"""
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.base_url}/{self.user_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
            'limit': min(limit, 100),  # Instagram API limit
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Filter posts that contain the hashtag
            hashtag_posts = []
            for post in data.get('data', []):
                caption = post.get('caption', '').lower()
                if f"#{hashtag.lower()}" in caption:
                    hashtag_posts.append(post)
                    
            return hashtag_posts
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Instagram media: {e}")
            return []
    
    def get_hashtag_top_media(self, hashtag_id: str, limit: int = 25) -> List[Dict]:
        """
        Get top media for a hashtag ID
        Note: Requires special permissions and hashtag ID resolution
        """
        self.rate_limiter.wait_if_needed()
        
        url = f"{self.base_url}/{hashtag_id}/top_media"
        params = {
            'user_id': self.user_id,
            'fields': 'id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count',
            'limit': min(limit, 50),
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching hashtag media: {e}")
            return []
    
    def calculate_engagement_rate(self, post: Dict) -> float:
        """Calculate engagement rate for a post"""
        likes = post.get('like_count', 0)
        comments = post.get('comments_count', 0)
        
        # Simple engagement calculation
        # In production, you'd want follower count for accurate rate
        total_engagement = likes + (comments * 2)  # Weight comments more
        
        # For now, return a normalized score based on engagement
        # This is a simplified approach for the MVP
        return min(total_engagement / 1000, 1.0)  # Normalize to 0-1


class RateLimiter:
    """Simple rate limiter to respect API limits"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
        
    def wait_if_needed(self):
        """Wait if we're approaching rate limits"""
        now = time.time()
        
        # Remove old requests outside the window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.window_seconds]
        
        # If we're at the limit, wait
        if len(self.requests) >= self.max_requests:
            sleep_time = self.window_seconds - (now - self.requests[0]) + 1
            if sleep_time > 0:
                print(f"Rate limit reached. Waiting {sleep_time:.1f} seconds...")
                time.sleep(sleep_time)
                
        # Record this request
        self.requests.append(now)