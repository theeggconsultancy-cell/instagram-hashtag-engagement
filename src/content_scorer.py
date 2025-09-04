from typing import Dict, List
from datetime import datetime, timedelta
import re

class ContentScorer:
    """Score and filter Instagram posts based on engagement and relevance"""
    
    def __init__(self, min_engagement_rate: float = 0.02):
        self.min_engagement_rate = min_engagement_rate
        
    def score_post(self, post: Dict) -> float:
        """Calculate a relevance score for a post (0-1)"""
        score = 0.0
        
        # Engagement rate (40% of score)
        engagement_rate = self._calculate_engagement_rate(post)
        score += engagement_rate * 0.4
        
        # Freshness (30% of score)
        freshness_score = self._calculate_freshness_score(post)
        score += freshness_score * 0.3
        
        # Caption quality (20% of score)
        caption_score = self._calculate_caption_score(post)
        score += caption_score * 0.2
        
        # Media type preference (10% of score)
        media_score = self._calculate_media_score(post)
        score += media_score * 0.1
        
        return min(score, 1.0)
    
    def filter_posts(self, posts: List[Dict]) -> List[Dict]:
        """Filter posts based on minimum criteria"""
        filtered_posts = []
        
        for post in posts:
            # Check minimum engagement rate
            engagement_rate = self._calculate_engagement_rate(post)
            if engagement_rate < self.min_engagement_rate:
                continue
                
            # Check if post is not too old (within last 7 days)
            if not self._is_recent(post):
                continue
                
            # Add score to post
            post['engagement_score'] = self.score_post(post)
            filtered_posts.append(post)
        
        # Sort by score (highest first)
        filtered_posts.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return filtered_posts
    
    def _calculate_engagement_rate(self, post: Dict) -> float:
        """Calculate engagement rate for a post"""
        likes = post.get('like_count', 0)
        comments = post.get('comments_count', 0)
        
        # Simple engagement calculation
        total_engagement = likes + (comments * 3)  # Weight comments more
        
        # Normalize to 0-1 (this is simplified for MVP)
        # In production, you'd use follower count or view count
        return min(total_engagement / 10000, 1.0)
    
    def _calculate_freshness_score(self, post: Dict) -> float:
        """Calculate freshness score based on post age"""
        timestamp_str = post.get('timestamp', '')
        if not timestamp_str:
            return 0.0
            
        try:
            post_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = datetime.now(post_time.tzinfo)
            age_hours = (now - post_time).total_seconds() / 3600
            
            # Posts are fresher if they're newer
            # Score decreases linearly over 72 hours
            if age_hours <= 24:
                return 1.0
            elif age_hours <= 72:
                return 1.0 - ((age_hours - 24) / 48)
            else:
                return 0.1  # Very old posts get minimal score
                
        except (ValueError, TypeError):
            return 0.0
    
    def _calculate_caption_score(self, post: Dict) -> float:
        """Calculate caption quality score"""
        caption = post.get('caption', '').lower()
        if not caption:
            return 0.2  # Posts without captions get low score
            
        score = 0.5  # Base score
        
        # Longer captions with substance get higher scores
        if len(caption) > 100:
            score += 0.2
        if len(caption) > 300:
            score += 0.1
            
        # Check for engagement-driving elements
        if any(word in caption for word in ['?', 'what', 'how', 'why', 'think', 'opinion']):
            score += 0.1  # Questions drive engagement
            
        # Reduce score for spam indicators
        hashtag_count = len(re.findall(r'#\w+', caption))
        if hashtag_count > 10:
            score -= 0.2  # Too many hashtags
            
        if any(spam_word in caption for spam_word in ['dm me', 'click link', 'buy now', 'limited time']):
            score -= 0.3  # Spam indicators
            
        return max(score, 0.0)
    
    def _calculate_media_score(self, post: Dict) -> float:
        """Calculate media type preference score"""
        media_type = post.get('media_type', '').upper()
        
        # Preference order for engagement
        if media_type == 'VIDEO':
            return 1.0
        elif media_type == 'IMAGE':
            return 0.8
        elif media_type == 'CAROUSEL_ALBUM':
            return 0.9
        else:
            return 0.5
    
    def _is_recent(self, post: Dict, max_age_days: int = 7) -> bool:
        """Check if post is recent enough"""
        timestamp_str = post.get('timestamp', '')
        if not timestamp_str:
            return False
            
        try:
            post_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = datetime.now(post_time.tzinfo)
            age = now - post_time
            return age <= timedelta(days=max_age_days)
            
        except (ValueError, TypeError):
            return False