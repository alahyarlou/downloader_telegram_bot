# Telegram File Downloader Bot

A simple Telegram bot built with **Python** and **pyTelegramBotAPI** that downloads files from direct HTTP/HTTPS URLs and sends them back to the user.

## Features

- 📥 Download files from direct URLs
- 📤 Upload downloaded files back to Telegram
- 🔍 URL validation
- 📄 Automatic filename detection
- 🏷️ Detect file extensions from the HTTP `Content-Type` header
- 🆔 Generate unique filenames when the URL has no filename
- 🧹 Automatically remove downloaded files after sending
- ⚠️ Error handling for invalid URLs and download failures
- 📝 Logging support

---

## Requirements

- Python 3.10+
- Telegram Bot Token

---

## Installation

Clone the repository:

```bash
git clone https://github.com/alahyarlou/downloader_telegram_bot.git

cd downloader_telegram_bot
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root.

```env
API_KEY=YOUR_TELEGRAM_BOT_TOKEN
```

Get your bot token from **@BotFather**.

---

## Running the Bot

```bash
python bot.py
```

When the bot starts you'll see:

```
Bot started...
```

---

## Usage

1. Start the bot.

```
/start
```

2. Send a direct download URL.

Example:

```
https://example.com/file.pdf
```

The bot will:

- Validate the URL
- Download the file
- Send the file back to you
- Delete the temporary file

---

## Project Structure

```
.
├── bot.py
├── downloads/
├── .env
├── requirements.txt
└── README.md
```

---

## Dependencies

- pyTelegramBotAPI
- requests
- python-decouple

Install manually:

```bash
pip install pyTelegramBotAPI requests python-decouple
```

---

## How It Works

1. User sends a download link.
2. The bot validates the URL.
3. A temporary status message is displayed.
4. The file is downloaded into the `downloads/` directory.
5. The bot uploads the file back to the user.
6. The temporary file is removed.

---

## Supported URLs

Any direct HTTP or HTTPS file URL.

Examples:

```
https://example.com/image.jpg
```

```
https://example.com/video.mp4
```

```
https://example.com/archive.zip
```

---

## Limitations

- Only supports **direct download links**.
- Does **not** support:
  - Google Drive share links
  - Dropbox share links
  - Mega links
  - YouTube URLs
  - Streaming websites
- Telegram Bot API has upload size limits. Very large files cannot be sent by the bot.

---

## Future Improvements

- Background downloads using Celery + Redis
- Download progress updates
- Queue management
- Multiple concurrent downloads
- Docker support
- SQLite/PostgreSQL download history
- Rate limiting
- Retry failed downloads
- Admin panel
- Async implementation

---

## License

This project is licensed under the MIT License.

---

## Contributing

Contributions, issues, and pull requests are welcome.

If you find a bug or have an idea for a new feature, feel free to open an issue.

---

## Author

Made with ❤️ using Python and the Telegram Bot API.
