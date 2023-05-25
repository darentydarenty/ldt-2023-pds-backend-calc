import asyncio

import app

app = asyncio.get_running_loop().run_until_complete(app.App.build())

