from pyrogram import Client, filters , ContinuePropagation
import asyncio
from typing import List, Optional
from pyrogram.types import Message
import sqlite3

from config import api_hash , api_id ,bot_token , phone_number

SOURCE_CHANNEL = "fake_akharin"
FIRST_TARGET_CHANNEL = "TestAchannelA"
SECOND_TARGET_CHANNEL = "sendtochannel"

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


conn = sqlite3.connect('first_media_group_id')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS media_group_id (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER NOT NULL UNIQUE
    )
''')

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


def add_group_id(group_id):
    try:
        cursor.execute(
            'INSERT INTO media_group_id (group_id) VALUES (?)',
            (str(group_id),)  # Convert to string and fix tuple syntax
        )
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"error to add group id {group_id}")


def check_number(number_to_check):
    cursor.execute(
        'SELECT group_id FROM media_group_id WHERE group_id = ?', 
        (str(number_to_check),)
    )
    result = cursor.fetchone()
    if result is None:
        return False
    else:
        return True

client = Client("robot", api_id, api_hash ,proxy=proxy , phone_number=phone_number)
print("program started")




@client.on_message(filters.chat(SOURCE_CHANNEL))
async def all_message(_:Client , m:Message ):
    if m.media_group_id is None :
        print("1")
        await asyncio.sleep(5)
        await client.copy_message(
        chat_id=FIRST_TARGET_CHANNEL ,
        from_chat_id =SOURCE_CHANNEL,
        message_id=m.id
        )
    if m.media_group_id is not None  and check_number(m.media_group_id)== False:
        print("2")
        add_group_id(m.media_group_id)
        await asyncio.sleep(5)
        await client.copy_media_group(
            chat_id= FIRST_TARGET_CHANNEL,
            from_chat_id =SOURCE_CHANNEL,
            message_id=m.id
            )

@client.on_message(filters.chat(FIRST_TARGET_CHANNEL))
async def edit_message(_: Client, message: Message):
    """Handle incoming messages and replace tags if necessary."""
    print("edit func")
    # Handle text messages
    if message.text:
        modified_text = await replace_tags(message.text)
        await client.edit_message_text(
            FIRST_TARGET_CHANNEL,
            message.id,
            modified_text
        )
    
    # Handle captions
    if message.caption:
        modified_caption = await replace_tags(message.caption)
        await app.edit_message_caption(
            config.target_channel,
            message.id,
            modified_caption
        )


client.run()
