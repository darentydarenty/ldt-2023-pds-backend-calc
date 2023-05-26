import asyncio

import uvicorn

import app as a


app = a.App().get_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)