import asyncio

import app

app = asyncio.get_event_loop().run_until_complete(app.App.build())

