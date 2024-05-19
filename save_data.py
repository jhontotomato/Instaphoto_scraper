import aiofiles.os
from request_photo import fetch_photo
import pandas as pd
import aiofiles
from dataclasses import asdict
from Data_classes import PhotoData,DataPaths 
from tqdm import tqdm
import os

async def save_buffer(photo_data: dict[PhotoData], file_path: str, bar: tqdm):
    if photo_data is not None:
        
        if os.path.exists(file_path):

            # Conver list data to list[dict] to be saved and worked with.
            photo_data = [asdict(photo_data[i]) for i in range(len(photo_data))]
            
            # Get images and return data to be saved.
            cleaned_data = await save_images(photo_data, bar)
            
            # Read Old and Create a new Dataframe with new the new data.
            main_df = pd.read_parquet(file_path,engine='fastparquet')
            new_data = pd.DataFrame.from_dict(cleaned_data)
            
            # Append the new user information
            updated_parquet = pd.concat([main_df,new_data],ignore_index=True)

            # Save the updated DataFrame to Parquet
            updated_parquet.to_parquet(file_path, index=False,engine='fastparquet')
            
            bar.set_description("New data saved.")
            
            bar.update(1)
        else:
            await save_new_df(photo_data,file_path,bar)

async def save_new_df(photo_data: list[PhotoData],file_path,bar)-> None:
    
    photo_data: list[dict] = [asdict(photo_data[i]) for i in range(len(photo_data))]
    
    cleaned_data = await save_images(photo_data,bar)
    
    df = pd.DataFrame.from_dict(cleaned_data)
    
    df.to_parquet(file_path,index=False,engine='fastparquet')
    

async def save_images(photo_data: list[dict], bar: tqdm) -> list[dict]:
    num = 0
    
    to_save_data = []
    for data in photo_data:
        path = await mkdir_for_images(data['username'])
        
        # Generate a unique filename for each image
        image_path = os.path.join(path, f'{data["username"]}_{num}.jpeg')
        
        if not os.path.exists(image_path):
            
            image = await fetch_photo(data['photo_href'], bar)
            
            async with aiofiles.open(image_path, 'wb') as f:
                await f.write(image)
            bar.set_description('Image saved successfully.')
            
        # Remove the link column as is no longer relevant info
        data.pop('photo_href')
        data.update({'image_path':image_path})
        
        to_save_data.append(data)
        num += 1
        
    return to_save_data

async def mkdir_for_images(username:str):
    save_path = os.path.join(DataPaths.save_path,username)
    
    try:
        os.mkdir(save_path)
        return save_path
    except FileExistsError:
        return save_path

if __name__ == "__main__":
    pass