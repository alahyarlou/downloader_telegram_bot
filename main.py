import logging
import mimetypes
import os
import uuid
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
import telebot
from decouple import config

logger = telebot.logger

API_KEY = str(config("API_KEY"))

bot = telebot.TeleBot(API_KEY)
telebot.logger.setLevel(logging.INFO)

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message, "آدرس فایل موردنظر را ارسال کنید تا دانلود و برایتان ارسال شود."
    )


# Helper function
def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc


def downloder_file(url: str) -> Path:
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, stream=True, timeout=30, headers=headers)

    response.raise_for_status()
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)
    filename = unquote(filename)

    content_type = response.headers.get("Content-Type", "").split(";")[0]
    extension = mimetypes.guess_extension(content_type) or ""
    if not filename:
        filename = f"{uuid.uuid4().hex}{extension}"

    if extension and not Path(filename).suffix:
        filename += extension

    file_path = DOWNLOAD_DIR / filename

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return file_path


@bot.message_handler(func=lambda message: True)
def download_file(message):
    url = message.text.strip()

    if not is_valid_url(url):
        bot.reply_to(message, "❌ لینک معتبر نیست.")
        return

    bot.send_chat_action(message.chat.id, "upload_document")

    status_message = bot.reply_to(message, "⏳ در حال دانلود...")

    try:
        file_path = downloder_file(url)

        bot.edit_message_text(
            "✅ دانلود انجام شد. در حال ارسال فایل...",
            chat_id=status_message.chat.id,
            message_id=status_message.message_id,
        )

        with open(file_path, "rb") as document:
            bot.send_document(
                chat_id=message.chat.id,
                document=document,
                reply_to_message_id=message.message_id,
            )
        bot.delete_message(
            chat_id=status_message.chat.id,
            message_id=status_message.message_id,
        )
        file_path.unlink(missing_ok=True)
    except requests.exceptions.RequestException as e:
        logger.exception(e)
        bot.edit_message_text(
            "❌ دانلود فایل با خطا مواجه شد.",
            chat_id=status_message.chat.id,
            message_id=status_message.message_id,
        )

    except Exception as e:
        logger.exception(e)
        bot.edit_message_text(
            f"❌ Error:\n{e}",
            chat_id=status_message.chat.id,
            message_id=status_message.message_id,
        )


if __name__ == "__main__":
    logger.info("Bot started...")
    bot.infinity_polling(skip_pending=True)
