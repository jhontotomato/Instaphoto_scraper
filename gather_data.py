from Data_classes import PhotoData
from bs4 import BeautifulSoup

async def parse_content(html    :str):
    return BeautifulSoup(html,'html.parser')

async def get_data(html: str, username: str):
    if html != None:
        soup = await parse_content(html)
        
        links = [link['src'] for link in soup.find_all('img')]
        likes = [int(''.join(filter(str.isdigit, x.get_text(strip=True)))) for x in soup.find_all('div', class_='likes_photo')]
        descriptions = [link.get('alt') for link in soup.find_all('img')]
        comments = [int(''.join(filter(str.isdigit, x.get_text(strip=True)))) for x in soup.find_all('div', class_='comments_photo')]
        times = [x.get_text(strip=True) for x in soup.find_all('div', class_='time')]
        
        data = []
        for link, like_count, comment_count, time, description in zip(links, likes, comments, times, descriptions):
            data.append(PhotoData(
                username=username,
                photo_href=link,
                likes=int(like_count),
                description=description,
                comments=int(comment_count),
                date_posted=time
            ))
        if not data:
            return None
        else:
            return data

if __name__ == "__main__":
    pass