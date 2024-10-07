from pyrogram import Client, filters , ContinuePropagation
import asyncio
from typing import List, Optional
from pyrogram.types import Message


from config import api_hash , api_id ,bot_token , phone_number , SOURCE_CHANNEL ,FIRST_TARGET_CHANNEL,SECOND_TARGET_CHANNEL


TAGS_TO_REPLACE = [
    "@akharinkhabar | akharinkhabar.ir",
    "@akharinkhabar |akharinkhabar.ir",
    "@Akharinkhabar |akharinkhabar.ir",
    "@Akharinkhabar | akharinkhabar.ir"
]
REPLACEMENT_TAG = "@kiuskonline"


proxy = {
    "scheme": "http", 
    "hostname": "127.0.0.1",
    "port": 12334,

}



def replace_tags(text: str) -> str:
    """Replace all matching tags in the given text."""
    if not text:
        return text
        
    modified_text = text
    for tag in TAGS_TO_REPLACE:
        if tag in modified_text:
            modified_text = modified_text.replace(tag, REPLACEMENT_TAG)
            break
    return modified_text


client = Client("robot2", api_id, api_hash ,proxy=proxy , phone_number=phone_number)
print("program started")


@client.on_message(filters.chat(FIRST_TARGET_CHANNEL))
async def edit_message(_: Client, message: Message):
    """Handle incoming messages and replace tags if necessary."""
    print("edit func")
    # Handle text messages
    if message.text:
        modified_text = replace_tags(message.text)
        await client.edit_message_text(
            FIRST_TARGET_CHANNEL,
            message.id,
            modified_text
        )
    
    # Handle captions
    if message.caption:
        modified_caption = replace_tags(message.caption)
        await client.edit_message_caption(
            FIRST_TARGET_CHANNEL,
            message.id,
            modified_caption
        )


client.run()
