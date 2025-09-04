import asyncio
from typing import Dict, List
from telegram import Bot
from telegram.error import TelegramError
from .config import Config

class TelegramNotifier:
    """Send notifications via Telegram"""
    
    def __init__(self):
        self.bot_token = Config.TELEGRAM_BOT_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.bot = Bot(token=self.bot_token)
    
    async def send_post_notification(self, post: Dict):
        """Send a notification for a single high-quality post"""
        try:
            message = self._format_post_message(post)
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
            
            # If there's a media URL, send the media
            media_url = post.get('media_url')
            if media_url and post.get('media_type') == 'IMAGE':
                try:
                    await self.bot.send_photo(
                        chat_id=self.chat_id,
                        photo=media_url,
                        caption=f"🖼️ Post preview"
                    )
                except TelegramError:
                    # If image sending fails, just continue
                    pass
                    
        except TelegramError as e:
            print(f"Failed to send Telegram notification: {e}")
    
    async def send_batch_notification(self, posts: List[Dict]):
        """Send a batch notification with multiple posts"""
        if not posts:
            return
            
        try:
            message = self._format_batch_message(posts)
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=False
            )
        except TelegramError as e:
            print(f"Failed to send batch notification: {e}")
    
    async def send_status_notification(self, message: str):
        """Send a status/error notification"""
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"📊 <b>Hashtag Monitor Status</b>\n\n{message}",
                parse_mode='HTML'
            )
        except TelegramError as e:
            print(f"Failed to send status notification: {e}")
    
    def _format_post_message(self, post: Dict) -> str:
        """Format a single post for Telegram"""
        caption = post.get('caption', '')
        # Truncate caption if too long
        if len(caption) > 200:
            caption = caption[:200] + "..."
        
        engagement_score = post.get('engagement_score', 0)
        likes = post.get('like_count', 0)
        comments = post.get('comments_count', 0)
        permalink = post.get('permalink', '')
        
        message = f"""🎯 <b>High-Quality Post Found!</b>

📝 <b>Caption:</b> {caption}

📊 <b>Engagement:</b>
• Score: {engagement_score:.2f}
• Likes: {likes:,}
• Comments: {comments:,}

🔗 <b>Link:</b> <a href="{permalink}">View Post</a>

💡 <i>Click the link to engage manually</i>"""
        
        return message
    
    def _format_batch_message(self, posts: List[Dict]) -> str:
        """Format multiple posts for Telegram"""
        message = f"📋 <b>Daily Hashtag Report</b>\n\n"
        message += f"Found {len(posts)} high-quality posts:\n\n"
        
        for i, post in enumerate(posts[:5], 1):  # Limit to top 5 for readability
            caption = post.get('caption', '')[:100] + "..." if len(post.get('caption', '')) > 100 else post.get('caption', '')
            score = post.get('engagement_score', 0)
            likes = post.get('like_count', 0)
            permalink = post.get('permalink', '')
            
            message += f"""<b>{i}.</b> Score: {score:.2f} | ❤️ {likes}
📝 {caption}
🔗 <a href="{permalink}">View Post</a>

"""
        
        if len(posts) > 5:
            message += f"... and {len(posts) - 5} more posts"
            
        return message
    
    def send_notification_sync(self, post: Dict):
        """Synchronous wrapper for sending notifications"""
        try:
            asyncio.run(self.send_post_notification(post))
        except Exception as e:
            print(f"Error sending notification: {e}")
    
    def send_batch_sync(self, posts: List[Dict]):
        """Synchronous wrapper for sending batch notifications"""
        try:
            asyncio.run(self.send_batch_notification(posts))
        except Exception as e:
            print(f"Error sending batch notification: {e}")
    
    def send_status_sync(self, message: str):
        """Synchronous wrapper for sending status notifications"""
        try:
            asyncio.run(self.send_status_notification(message))
        except Exception as e:
            print(f"Error sending status notification: {e}")