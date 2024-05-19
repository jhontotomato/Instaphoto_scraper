import os
import pandas as pd
from dataclasses import dataclass, field

@dataclass  
class SessionData:
    picuki_url: str = 'https://www.picuki.com/profile/'
    headers = {"Content-Type": "application/json","User-Agent": "insomnia/8.6.1"}
    _usernames: set = field(init=False)
    userinfo_url: set = field(init=False) 
    Timeout: int = 60
    qued_wait: int = 3
    
    def __post_init__(self):
        self._usernames = self.load_usernames() 
        self.userinfo_url = self.generate_urls()
    
    def load_usernames(self):
        usernames_df = pd.read_parquet(DataPaths.trans_results_df,engine='fastparquet').query('public_email.notna()')
        
        if os.path.exists(DataPaths.photo_results_df):
            photo_results_df = pd.read_parquet(DataPaths.photo_results_df,columns=['username'],engine='fastparquet')

            return set(usernames_df['username']).difference(set(photo_results_df['username']))
        
        return set(usernames_df['username'])

    def generate_urls(self):
        return [self.picuki_url + user for user in self._usernames]
        


@dataclass
class DataPaths:
    photo_results_df = r'j:/python_projects/Instaphoto_scraper/photo_scrape_results.parquet'
    save_path = r'j:/python_projects/Instaphoto_scraper/user_photos'
    scrape_results = r"j:/python_projects\snapscrape\Data_frames\scrape_results.parquet"
    trans_results_df = r"j:/python_projects/Snapscrape/Data_frames/trans_results.parquet"

@dataclass
class PhotoData:
    username: str
    photo_href: str
    description: str
    likes: int
    comments:int
    date_posted: str
    

if __name__ == "__main__":
    ses = SessionData()
    print(len(ses._usernames))
