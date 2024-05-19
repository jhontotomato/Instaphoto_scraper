import asyncio
import aiohttp
from Data_classes import SessionData
from tqdm import tqdm 

async def fetch_photo(url:str,bar: tqdm = False,sleep_time = 1):
    timeout = aiohttp.ClientTimeout(SessionData.Timeout)
    if bar:
        bar.set_description(f'Requesting: {url}')
        
    async with aiohttp.ClientSession(timeout=timeout,headers=SessionData.headers) as session:
        if not url.endswith('.jpeg'):
            await asyncio.sleep(sleep_time)
        
        return await request(session,url)
    
async def request(session, url: str):
    try :
        async with session.get(url) as response:
            if response.status == 200:
                if url.endswith('.jpeg'):
                    image = await response.read()
                    return image
                else:
                    _response = await response.read()
                
                if not _response:
                    pass
                else:
                    return _response
    except asyncio.TimeoutError as e:
        print(e)
        return None

if __name__ == "__main__":
    pass