import asyncio

from asgiref.sync import async_to_sync
from fastapi import FastAPI

import app as a

app = asyncio.create_task(a.App.build()).current_task().result()
