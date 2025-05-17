import time
import threading
from datetime import datetime
from client import TextNowClient, DIRECTION_OUTGOING, DIRECTION_INCOMING

def format_message(msg):
    """Format a message for display."""
    # Use numeric message direction (1 = outgoing, 2 = incoming)
    direction = "📨" if msg["message_direction"] == DIRECTION_OUTGOING else "📤"
    # Handle different date formats from the API
    date_str = msg.get("date", "")  # API uses 'date' field
    try:
        if date_str:
            # Parse ISO format date
            timestamp = datetime.strptime(date_str.split('T')[1].split('Z')[0], "%H:%M:%S").strftime("%H:%M:%S")
        else:
            timestamp = datetime.now().strftime("%H:%M:%S")
    except ValueError:
        timestamp = datetime.now().strftime("%H:%M:%S")
    
    msg_id = msg.get("id", "no_id")
    return f"{direction} [{timestamp}] ({msg_id}): {msg.get('message', '')}"

def show_conversation_history(client, phone_number):
    """Display recent conversation history."""
    print("\n📜 Recent conversation history:")
    print("------------------------------")
    messages = client.get_conversation(phone_number)
    if not messages:
        print("No recent messages found.")
    else:
        for msg in reversed(messages[-10:]):  # Show last 10 messages
            print(format_message(msg))
    print("------------------------------\n")

def message_listener(client, phone_number, stop_event):
    """Background thread to check for new messages."""
    print("🔄 Message listener started (polling silently)...")
    print("Ready to receive messages. Send a text to test!")
    
    while not stop_event.is_set():
        try:
            new_msgs = client.get_new_messages()
            
            # Show only incoming messages from our conversation
            # Direction 1 means it's from the contact (incoming to us)
            for msg in new_msgs:
                if (msg['contact_value'] == phone_number and 
                    msg['message_direction'] == DIRECTION_OUTGOING):  # 1 means from contact to us
                    print(f"\n{format_message(msg)}")
                    print("You: ", end='', flush=True)  # Restore input prompt
            
            time.sleep(2)  # Poll every 2 seconds
        except Exception as e:
            print(f"\n❌ Error in message listener: {str(e)}")
            time.sleep(5)  # Wait longer on error

def run_cli():
    """Main CLI interface."""
    client = TextNowClient()
    
    print("📱 TextNow CLI Client")
    print("--------------------")
    
    # Use hardcoded phone number
    phone = "+16137160016"
    print(f"Starting chat with: {phone}")
    
    # Show recent conversation history
    show_conversation_history(client, phone)
    
    # Create a stop event for the background thread
    stop_event = threading.Event()
    
    # Start the message listener in a background thread
    listener_thread = threading.Thread(
        target=message_listener,
        args=(client, phone, stop_event)
    )
    listener_thread.daemon = True
    listener_thread.start()
    
    print("💬 Chat started! Type your message or '/exit' to quit.")
    print("Type '/help' for available commands.\n")
    
    try:
        while True:
            message = input("You: ").strip()
            
            if not message:
                continue
                
            if message.lower() == '/exit':
                break
                
            if message.lower() == '/help':
                print("\nAvailable commands:")
                print("  /exit - Exit the chat")
                print("  /help - Show this help message")
                print("  /history - Show recent conversation history")
                print("  /status - Show listener status")
                continue
                
            if message.lower() == '/history':
                show_conversation_history(client, phone)
                continue
                
            if message.lower() == '/status':
                print("\n🔍 Checking message listener status...")
                print(f"Last check time: {client.last_check_time.strftime('%H:%M:%S')}")
                print(f"Seen messages: {len(client.seen_message_ids)}")
                continue
                
            # Send regular message
            client.send_sms(phone, message)
                
    except KeyboardInterrupt:
        print("\nExiting chat...")
    
    # Clean up
    stop_event.set()
    listener_thread.join(timeout=1)

if __name__ == "__main__":
    run_cli() 