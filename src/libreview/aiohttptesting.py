import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession(base_url='http://httpbin.org') as session:
        async with session.get('/get') as resp:
            print(resp.status)
            print(await resp.text())
        session._base_url = "https://api.libreview.io"
        session._default_headers = {"connection": "Keep-Alive"}
        async with session.get('/account') as resp:
            print(resp.status)
            print(await resp.text())
        

asyncio.run(main())