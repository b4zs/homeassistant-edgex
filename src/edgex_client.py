import aiohttp
import asyncio
import os


EDGEX_CORE_DATA_URL = os.getenv("EDGEX_CORE_DATA_URL")

async def push_data(data):
    headers = {
        "Content-Type": "application/json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(EDGEX_CORE_DATA_URL, json=data, headers=headers) as response:
            return response.status

