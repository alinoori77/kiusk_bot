from pyrogram import Client, filters , ContinuePropagation
import asyncio
from typing import List, Optional
from pyrogram.types import Message
import sqlite3

from config import api_hash , api_id, phone_number , SOURCE_CHANNEL ,FIRST_TARGET_CHANNEL,SECOND_TARGET_CHANNEL

TAGS_TO_REPLACE = [
    "@akharinkhabar | akharinkhabar.ir",
    "@akharinkhabar |akharinkhabar.ir",
    "@Akharinkhabar |akharinkhabar.ir",
    "@Akharinkhabar | akharinkhabar.ir"
]
REPLACEMENT_TAG = "@kiuskonline"


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

client = Client("robot1",api_hash=api_hash , api_id=api_id, phone_number=phone_number)
print("program bot 1 started")


@client.on_message(filters.chat(SOURCE_CHANNEL))
async def all_message(_:Client , m:Message ):

    if m.media_group_id is None :
        await asyncio.sleep(5)
        await client.copy_message(
        chat_id=FIRST_TARGET_CHANNEL ,
        from_chat_id =SOURCE_CHANNEL,
        message_id=m.id
        )
    if m.media_group_id is not None  and check_number(m.media_group_id)== False:
        add_group_id(m.media_group_id)
        await asyncio.sleep(5)
        await client.copy_media_group(
            chat_id= FIRST_TARGET_CHANNEL,
            from_chat_id =SOURCE_CHANNEL,
            message_id=m.id
            )



client.run()
