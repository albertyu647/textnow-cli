# TextNow CLI Client

A command-line interface for sending and receiving messages through TextNow.

## Features
- Send and receive text messages from the terminal
- Real-time message notifications
- Clean and intuitive interface
- Command history and conversation view

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

3. Create a `.env` file in the project root with your TextNow credentials:
```bash
TEXTNOW_USERNAME=your_username_here
TEXTNOW_SID_COOKIE=your_sid_cookie_here
TEXTNOW_CSRF_TOKEN=your_csrf_token_here
```

To get your credentials:
1. Log into TextNow in your browser
2. Open Developer Tools (F12)
3. Go to Application > Cookies > textnow.com
4. Find and copy:
   - `connect.sid` value for `TEXTNOW_SID_COOKIE`
   - `_csrf` value for `TEXTNOW_CSRF_TOKEN`
   Your username is your TextNow username

## Usage

Run the client:
```bash
python main.py
```

Available commands:
- `/help` - Show available commands
- `/exit` - Exit the chat
- `/history` - Show recent conversation history
- `/status` - Show listener status

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/) 