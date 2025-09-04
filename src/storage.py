import json
import os
from typing import Dict, List, Set
from datetime import datetime
from .config import Config

class StorageManager:
    """Manage storage of processed posts and configuration"""
    
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        self.processed_posts_file = Config.PROCESSED_POSTS_FILE
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_processed_posts(self) -> Set[str]:
        """Get set of processed post IDs"""
        if not os.path.exists(self.processed_posts_file):
            return set()
        
        try:
            with open(self.processed_posts_file, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_post_ids', []))
        except (json.JSONDecodeError, IOError):
            return set()
    
    def mark_posts_processed(self, post_ids: List[str]):
        """Mark posts as processed"""
        processed_posts = self.get_processed_posts()
        processed_posts.update(post_ids)
        
        data = {
            'processed_post_ids': list(processed_posts),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.processed_posts_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"Error saving processed posts: {e}")
    
    def is_post_processed(self, post_id: str) -> bool:
        """Check if a post has been processed"""
        return post_id in self.get_processed_posts()
    
    def cleanup_old_processed_posts(self, days_to_keep: int = 30):
        """Clean up old processed post IDs to prevent file from growing too large"""
        # For now, we'll just keep all posts
        # In production, you might want to implement a cleanup strategy
        pass
    
    def save_posts_data(self, posts: List[Dict], filename: str = None):
        """Save posts data for debugging/analysis"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"posts_data_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(posts, f, indent=2, default=str)
            print(f"Posts data saved to {filepath}")
        except IOError as e:
            print(f"Error saving posts data: {e}")
    
    def get_stats(self) -> Dict:
        """Get storage statistics"""
        processed_count = len(self.get_processed_posts())
        
        return {
            'processed_posts_count': processed_count,
            'data_directory': self.data_dir,
            'files': os.listdir(self.data_dir) if os.path.exists(self.data_dir) else []
        }