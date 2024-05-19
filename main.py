from dataclasses import dataclass
import os
from tqdm import tqdm
from Data_classes import SessionData,DataPaths
from request_photo import fetch_photo
from gather_data import get_data
from save_data import save_buffer
import asyncio

async def main():
    session = SessionData()
    
    urls = session.userinfo_url
    
    bar = tqdm(total=len(urls))
    
    tasks = []
    for url in urls:
        username = os.path.basename(url)
        fetched_data = asyncio.create_task(fetch_photo(url,bar,1))
        data = asyncio.create_task(get_data(await fetched_data,username))
        save = asyncio.create_task(save_buffer(await data,DataPaths.photo_results_df, bar))
        
        tasks.append(fetched_data)
        tasks.append(data)
        tasks.append(save)
        
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())