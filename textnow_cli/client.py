import cloudscraper
import config
import time
from datetime import datetime, timedelta
import json  # for pretty printing debug info
import os

# Message direction constants
# In the API:
# 1 = message from contact to us (incoming)
# 2 = message from us to contact (outgoing)
DIRECTION_OUTGOING = 1  # When contact sends to us
DIRECTION_INCOMING = 2  # When we send to contact

class TextNowClient:
    def __init__(self, username=None, sid_cookie=None, csrf_token=None):
        self.username = username or config.USERNAME
        self.sid_cookie = sid_cookie or config.SID_COOKIE
        self.csrf_token = csrf_token or config.CSRF_TOKEN
        self.seen_message_ids = set()  # Track seen message IDs
        self.last_check_time = datetime.now()
        self.last_message_id = None  # Track the last message ID we've seen
        
        # Initialize cloudscraper
        self.scraper = cloudscraper.create_scraper(browser={
            'browser': 'chrome',
            'platform': 'darwin',
            'mobile': False
        })
        
        # Set headers
        self.scraper.headers.update({
            "User-Agent": config.USER_AGENT,
            "x-csrf-token": self.csrf_token,
            "x-requested-with": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Referer": "https://www.textnow.com/messaging"
        })
        
        # Set cookies
        self.scraper.cookies.set("connect.sid", self.sid_cookie, domain=".textnow.com")
        self.scraper.cookies.set("_csrf", self.csrf_token, domain=".textnow.com")

    def _debug_response(self, response, method="GET"):
        """Debug helper to print API response details"""
        if os.getenv('TEXTNOW_DEBUG'):
            print(f"\n🔍 DEBUG: {method} {response.url}")
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            try:
                data = response.json()
                print(f"Response: {json.dumps(data, indent=2)}")
            except:
                print(f"Raw response: {response.text[:500]}")

    def send_sms(self, to_number, message_text):
        """Send an SMS message to a phone number."""
        url = f"{config.BASE_URL}/users/{self.username}/messages"
        payload = {
            "contact_value": to_number,
            "message": message_text,
            "message_direction": DIRECTION_INCOMING,  # 2 = from us to contact
            "message_type": 1  # 1 = text message
        }
        
        try:
            response = self.scraper.post(url, data=payload)
            if response.status_code == 200:
                print("📤 Message sent successfully")
                return True
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                self._debug_response(response, "POST")
                return False
        except Exception as e:
            print(f"❌ Error sending message: {str(e)}")
            return False

    def _parse_message_date(self, msg):
        """Parse message date from various possible fields."""
        date_str = msg.get("date_created", msg.get("created_at", ""))
        if not date_str:
            return datetime.now()
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.now()

    def get_new_messages(self):
        """Fetch new messages from TextNow."""
        url = f"{config.BASE_URL}/users/{self.username}/messages"
        
        try:
            response = self.scraper.get(url)
            if response.status_code != 200:
                print(f"❌ Failed to fetch messages: {response.status_code}")
                return []

            data = response.json()
            messages = data.get("messages", [])
            new_messages = []

            if not messages:
                return []

            # Get latest message ID from response
            latest_msg = messages[0]  # API returns newest first
            latest_id = latest_msg.get("id")
            
            # On first run, just store the latest ID
            if self.last_message_id is None:
                self.last_message_id = latest_id
                return []

            # If we have new messages (higher IDs)
            if latest_id > self.last_message_id:
                # Add all messages with higher IDs
                for msg in messages:
                    msg_id = msg.get("id")
                    if msg_id and msg_id > self.last_message_id:
                        # Only show debug for incoming messages from contact
                        if msg.get('message_direction') == DIRECTION_OUTGOING:
                            print(f"\n🔍 Found new message from contact!")
                        new_messages.append(msg)
                self.last_message_id = latest_id

            return new_messages
            
        except Exception as e:
            print(f"❌ Error fetching messages: {str(e)}")
            return []

    def get_conversation(self, phone_number, limit=50):
        """Get recent conversation history with a specific number."""
        url = f"{config.BASE_URL}/users/{self.username}/messages"
        params = {
            "contact_value": phone_number,
            "page_size": limit
        }
        try:
            response = self.scraper.get(url, params=params)
            if response.status_code == 200:
                # Debug: print raw response
                print("\n📥 Conversation History Response:")
                self._debug_response(response)
                
                messages = response.json().get("messages", [])
                # Add message IDs to seen set to avoid re-displaying them
                for msg in messages:
                    if msg.get("id"):
                        self.seen_message_ids.add(msg.get("id"))
                return messages
            return []
        except Exception as e:
            print(f"❌ Error fetching conversation: {str(e)}")
            return [] 