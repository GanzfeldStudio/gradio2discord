import os
import sys
import aiohttp
import asyncio
import discord
import requests
from typing import Optional
from modules import script_callbacks, sd_models, shared, scripts

extension_name = os.path.basename(scripts.basedir())
extension_path = os.path.join(scripts.basedir())
scripts_path = os.path.join(scripts.basedir(), "scripts")

async def post_to_discord_click():
    discord_webhook = await read_file("discord_webhook.txt")
    sys.path.append(os.path.join(os.path.dirname(__file__), scripts.basedir(), "modules"))
    from shared import demo
    gradio_url = shared.demo.share_url
    previous_message_id = await read_file("previous_message_id.txt", int)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(discord_webhook, session=session)
        if previous_message_id is not None:
            try:
                message = await webhook.fetch_message(previous_message_id)
            except discord.errors.NotFound:
                print(f"Message with ID {previous_message_id} not found, sending new message...")
                message = await webhook.send(gradio_url, wait=True)
            else:
                await message.delete()
                message = await webhook.send(gradio_url, wait=True)
        else:
            message = await webhook.send(gradio_url, wait=True)
        print("gradio2discord extension shared public Gradio URL to Discord")
        await asyncio.sleep(1)  # Add a small delay here
        await write_file("previous_message_id.txt", message.id)
    await write_file("gradio_url.txt", gradio_url)

async def read_file(filename, return_type=str):
    try:
        with open(os.path.join(scripts_path, filename), "r") as f:
            return return_type(f.read().strip())
    except FileNotFoundError:
        return None

async def write_file(filename, contents):
    with open(os.path.join(scripts_path, filename), "w") as f:
        f.write(str(contents))

def run_post_to_discord_callback(demo, app):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(post_to_discord_click())

script_callbacks.on_app_started(run_post_to_discord_callback)
