import aiohttp
import asyncio
from decouple import config

async def test_proxy(proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.ipify.org?format=json',
                proxy=f"http://{proxy}",
                timeout=10
            ) as response:
                if response.status == 200:
                    return proxy
    except:
        pass
    return None

async def get_valid_proxies():
    proxy_list = config('PROXY_LIST', default='').split(',')
    tasks = [test_proxy(proxy) for proxy in proxy_list]
    results = await asyncio.gather(*tasks)
    return [proxy for proxy in results if proxy]

def validate_proxies():
    return asyncio.run(get_valid_proxies()) 