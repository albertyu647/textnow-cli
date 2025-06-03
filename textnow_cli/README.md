# TextNow CLI Client

A command-line interface for sending and receiving messages through TextNow with ChatGPT auto-reply.

## Features
- Send and receive text messages from the terminal
- 🤖 **ChatGPT auto-reply**: Text the TextNow number from your phone and get AI responses
- Real-time message notifications
- Clean and intuitive interface
- Command history and conversation view
- Switch between GPT-4o and o3-mini models

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/textnow-cli.git
cd textnow-cli
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your credentials:
```bash
TEXTNOW_USERNAME=your_username_here
TEXTNOW_SID_COOKIE=your_sid_cookie_here
TEXTNOW_CSRF_TOKEN=your_csrf_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

To get your credentials:

**TextNow:**
1. Log into TextNow in your browser
2. Open Developer Tools (F12)
3. Go to Application > Cookies > textnow.com
4. Find and copy:
   - `connect.sid` value for `TEXTNOW_SID_COOKIE`
   - `_csrf` value for `TEXTNOW_CSRF_TOKEN`
   Your username is your TextNow username

**OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key for `OPENAI_API_KEY`

## Usage

Run the client:
```bash
python main.py
```

### Terminal Commands:
- `/help` - Show available commands
- `/exit` - Exit the chat
- `/history` - Show recent conversation history
- `/status` - Show listener status

### Phone Commands (text these to your TextNow number):
- `/new` - Start new ChatGPT session
- `/model 4o` - Switch to GPT-4o
- `/model o3` - Switch to o3-mini
- `/help` - Show phone commands

## How It Works

1. Run the script on your computer
2. Text your TextNow number from your phone
3. ChatGPT automatically responds to your messages
4. Use commands to control the AI behavior

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/) 