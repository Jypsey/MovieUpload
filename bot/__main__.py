import random
import logging
from time import sleep
import traceback
import time
from pyrogram import filters
import os
import sys
from bot import app, monitored_chats, chats_map, sudo_users
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram import Client
import logging

logging.info("Bot Started")
BOT_START_TIME = time.time()

def get_file_id(msg: Message):
    if not msg.media: return None
    for message_type in ("photo", "animation", "audio", "document", "video", "video_note", "voice", "sticker"):
        obj = getattr(msg, message_type)
        if obj:
            setattr(obj, "message_type", message_type)
            return obj

blocked_words = ["aavesham"]
count=0
@app.on_message(filters.chat(monitored_chats) & filters.incoming)
def work(_: Client, message: Message):
    caption = None
    msg = None
    chat = chats_map.get(message.chat.id)
    custom_caption = "{filename}\ncoded by @stellarlabsowner"  # Custom caption template
    global count 
    if chat.get("replace"):
        for old, new in chat["replace"].items():
            if message.media and not message.poll:
                caption = message.caption.markdown.replace(old, new) if message.caption else None
            elif message.text:
                msg = message.text.markdown.replace(old, new)

    contains_required_word = False
    if caption and any(word in caption.lower() for word in blocked_words):
        contains_required_word = True
        count=count+1
    elif msg and any(word in msg.lower() for word in blocked_words):
        contains_required_word = True
        count=count+1

    try:
        for chat_id in chat["to"]:
            if contains_required_word:
                if message.media:
                    # Get the filename if available
                    filename = None
                    if message.document:
                        filename = message.document.file_name
                    elif message.video:
                        filename = message.video.file_name
                    elif message.audio:
                        filename = message.audio.file_name
                    
                    # Create the custom caption
                    custom_caption_formatted = custom_caption.format(filename=filename) if filename else custom_caption
                    
                    # Forward the message with the custom caption
                    message.copy(chat_id, caption=custom_caption_formatted, parse_mode=ParseMode.MARKDOWN)
                elif msg:
                    app.send_message(chat_id, msg, parse_mode=ParseMode.MARKDOWN)
                else:
                    message.copy(chat_id)
            else:
                logging.info(f"Message from {message.chat.id} does not contain required words, not forwarding.")
    except Exception as e:
        logging.error(f"Error while sending message from {message.chat.id} to {chat_id}: {e}")
if count==10:
    await self.send_message(chat_id, text="All Set 😇")
@app.on_message(filters.command("alive"))
async def alive_handler(client, message):
    await message.reply_text(f"aada njan chathitilla evide thanne inde😇")

app.run()
