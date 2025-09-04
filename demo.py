#!/usr/bin/env python3
"""
Demo script for Instagram Hashtag Engagement Monitor

This script demonstrates the system with mock data so users can see
how it works before setting up real credentials.
"""

import json
from datetime import datetime, timedelta
from src.content_scorer import ContentScorer
from src.notifier import TelegramNotifier
from src.storage import StorageManager

# Mock Instagram post data for demonstration
MOCK_POSTS = [
    {
        "id": "mock_post_1",
        "caption": "Just launched my new Python project! 🚀 What do you think about automated Instagram monitoring? #python #automation #webdev #coding",
        "media_type": "IMAGE",
        "media_url": "https://example.com/image1.jpg",
        "permalink": "https://instagram.com/p/mock1",
        "timestamp": (datetime.now() - timedelta(hours=2)).isoformat() + "Z",
        "like_count": 150,
        "comments_count": 12
    },
    {
        "id": "mock_post_2", 
        "caption": "Building awesome stuff with #programming and #tech. Check out this algorithm optimization! What's your favorite coding language?",
        "media_type": "VIDEO",
        "media_url": "https://example.com/video1.mp4",
        "permalink": "https://instagram.com/p/mock2",
        "timestamp": (datetime.now() - timedelta(hours=5)).isoformat() + "Z",
        "like_count": 89,
        "comments_count": 8
    },
    {
        "id": "mock_post_3",
        "caption": "Low engagement post with too many hashtags #one #two #three #four #five #six #seven #eight #nine #ten #eleven #twelve",
        "media_type": "IMAGE", 
        "media_url": "https://example.com/image2.jpg",
        "permalink": "https://instagram.com/p/mock3",
        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat() + "Z",
        "like_count": 5,
        "comments_count": 0
    },
    {
        "id": "mock_post_4",
        "caption": "Old post from yesterday #python #oldcontent",
        "media_type": "IMAGE",
        "media_url": "https://example.com/image3.jpg", 
        "permalink": "https://instagram.com/p/mock4",
        "timestamp": (datetime.now() - timedelta(days=2)).isoformat() + "Z",
        "like_count": 200,
        "comments_count": 25
    }
]

class MockInstagramClient:
    """Mock Instagram client for demonstration"""
    
    def search_hashtag(self, hashtag: str, limit: int = 25):
        """Return mock posts that contain the hashtag"""
        hashtag_posts = []
        for post in MOCK_POSTS:
            caption = post.get('caption', '').lower()
            if f"#{hashtag.lower()}" in caption:
                hashtag_posts.append(post.copy())
        return hashtag_posts

def demo_content_scoring():
    """Demonstrate content scoring functionality"""
    print("🎯 Content Scoring Demo")
    print("=" * 30)
    
    scorer = ContentScorer(min_engagement_rate=0.01)
    
    print(f"📊 Analyzing {len(MOCK_POSTS)} mock posts...")
    
    for i, post in enumerate(MOCK_POSTS, 1):
        score = scorer.score_post(post)
        engagement_rate = scorer._calculate_engagement_rate(post)
        
        print(f"\n📝 Post {i}: {post['caption'][:50]}...")
        print(f"   Score: {score:.2f}")
        print(f"   Engagement Rate: {engagement_rate:.3f}")
        print(f"   Likes: {post['like_count']}, Comments: {post['comments_count']}")
    
    # Filter posts
    filtered_posts = scorer.filter_posts(MOCK_POSTS.copy())
    
    print(f"\n✅ Filtered Results:")
    print(f"   Original posts: {len(MOCK_POSTS)}")
    print(f"   Posts passing filter: {len(filtered_posts)}")
    
    if filtered_posts:
        print(f"   Top post score: {filtered_posts[0]['engagement_score']:.2f}")

def demo_hashtag_search():
    """Demonstrate hashtag search functionality"""
    print("\n🔍 Hashtag Search Demo")
    print("=" * 30)
    
    client = MockInstagramClient()
    hashtags = ['python', 'programming', 'webdev', 'nonexistent']
    
    for hashtag in hashtags:
        posts = client.search_hashtag(hashtag)
        print(f"#{hashtag}: {len(posts)} posts found")

def demo_storage():
    """Demonstrate storage functionality"""
    print("\n💾 Storage Demo")
    print("=" * 30)
    
    storage = StorageManager()
    
    # Test marking posts as processed
    test_post_ids = ["demo_post_1", "demo_post_2", "demo_post_3"]
    storage.mark_posts_processed(test_post_ids)
    
    print(f"✅ Marked {len(test_post_ids)} posts as processed")
    
    # Check if posts are processed
    for post_id in test_post_ids:
        is_processed = storage.is_post_processed(post_id)
        print(f"   {post_id}: {'✅ Processed' if is_processed else '❌ Not processed'}")
    
    # Get stats
    stats = storage.get_stats()
    print(f"\n📊 Storage Stats:")
    print(f"   Processed posts: {stats['processed_posts_count']}")
    print(f"   Data directory: {stats['data_directory']}")

def demo_workflow():
    """Demonstrate the complete workflow with mock data"""
    print("\n🔄 Complete Workflow Demo")
    print("=" * 35)
    
    # Initialize components
    client = MockInstagramClient()
    scorer = ContentScorer(min_engagement_rate=0.01)
    storage = StorageManager()
    
    hashtags = ['python', 'programming']
    all_posts = []
    
    # Search hashtags
    for hashtag in hashtags:
        print(f"\n📍 Searching #{hashtag}...")
        posts = client.search_hashtag(hashtag)
        print(f"   Found {len(posts)} posts")
        
        # Filter out processed posts
        new_posts = []
        for post in posts:
            if not storage.is_post_processed(post['id']):
                new_posts.append(post)
        
        print(f"   {len(new_posts)} new posts (not processed)")
        all_posts.extend(new_posts)
    
    if not all_posts:
        print("💭 No new posts found")
        return
    
    # Score and filter
    print(f"\n📊 Scoring {len(all_posts)} posts...")
    filtered_posts = scorer.filter_posts(all_posts)
    print(f"   ✅ {len(filtered_posts)} posts passed quality filters")
    
    if filtered_posts:
        print(f"\n🏆 Top Posts:")
        for i, post in enumerate(filtered_posts[:3], 1):
            print(f"   {i}. Score: {post['engagement_score']:.2f} - {post['caption'][:50]}...")
        
        # Save demo data
        storage.save_posts_data(filtered_posts, "demo_filtered_posts.json")
        
        # Mark as processed
        post_ids = [post['id'] for post in all_posts]
        storage.mark_posts_processed(post_ids)
        print(f"✅ Marked {len(post_ids)} posts as processed")

def print_demo_intro():
    """Print demo introduction"""
    print("🎬 Instagram Hashtag Engagement Monitor - DEMO MODE")
    print("=" * 55)
    print("This demo shows how the system works with mock data.")
    print("No real Instagram API calls are made.")
    print("=" * 55)

def main():
    print_demo_intro()
    
    # Run demonstrations
    demo_content_scoring()
    demo_hashtag_search()
    demo_storage()
    demo_workflow()
    
    print("\n🎉 Demo completed!")
    print("\nTo use with real data:")
    print("1. Run: python setup.py")
    print("2. Configure your credentials in .env")
    print("3. Run: python monitor.py")

if __name__ == "__main__":
    main()