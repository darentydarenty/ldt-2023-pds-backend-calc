import asyncio

import app as a


async def app():
    return await a.App.build()

