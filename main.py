import asyncio

import nest_asyncio

import app
nest_asyncio.apply()
app = asyncio.get_event_loop().run_until_complete(app.App.build())

