import asyncio

import app

app = asyncio.create_task(app.App.build()).result()

