import asyncio
import aiohttp
from UTILITY import validate_token
from typing import Any

class InvalidToken(Exception):
    """invalid token passed"""
    pass

class Client:

    def __init__(self, token, session: aiohttp.ClientSession, channel_id, message_id=None):
        self.authentication = {"Authorization": token}

        if validate_token(token) is False:
            self.authentication = {"Authorization":f"Bot {token}"}
            if validate_token(token, True) is False:
                raise InvalidToken

        self.channel_id = channel_id
        self.message_id = message_id
        self.session = session

        self.edit_endpoint = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
        self.send_endpoint = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    async def send(self, content):
        payload = {
            "content": content
        }
        async with self.session.post(url=self.send_endpoint, json=payload, headers=self.authentication):
            return

    async def edit(self, content):
        payload = {
            "content": content
        }
        async with self.session.patch(url=self.edit_endpoint, json=payload, headers=self.authentication):
            return

    async def sendWithID(self, content):
        payload = {
            "content": content
        }
        async with self.session.post(url=self.send_endpoint, json=payload, headers=self.authentication) as response:
            response_json = await response.json()
            return response_json['id']