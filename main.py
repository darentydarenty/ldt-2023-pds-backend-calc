import asyncio

from asgiref.sync import async_to_sync

import app as a

@async_to_sync
async def app():
    return await a.App.build()

