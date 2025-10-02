import scrapetube
import json
import os
from datetime import datetime

DATA_FILE = 'data.json'

def parse_video(video):
    video_id = video.get('videoId')
    url = f"https://www.youtube.com/watch?v={video_id}"

    badges = video.get('badges', [])
    if 'LIVE' in badges:
        content_type = 'livestream'
    elif 'Premiered' in badges:
        content_type = 'premiere'
    else:
        content_type = 'video'

    title = video.get('title', {}).get('runs', [{}])[0].get('text')
    description = video.get('descriptionSnippet', {}).get('runs', [{}])[0].get('text')
    published = video.get('publishedTimeText', {}).get('simpleText')
    thumbnail = video.get('thumbnail', {}).get('thumbnails', [{}])[-1].get('url')
    views = video.get('viewCountText', {}).get('simpleText')

    return {
        'videoId': video_id,
        'url': url,
        'type': content_type,
        'title': title,
        'description': description,
        'published': published,
        'thumbnail': thumbnail,
        'views': views
    }

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def scrape_and_update(channel_id):
    print(f"Scraping channel: {channel_id}")
    videos = scrapetube.get_channel(channel_id)
    new_data = [parse_video(v) for v in videos]

    def sort_key(v):
        try:
            return datetime.strptime(v['published'], "%b %d, %Y")
        except:
            return datetime.min

    new_data.sort(key=sort_key, reverse=True)

    existing_data = load_existing_data()
    existing_ids = {v['videoId'] for v in existing_data}
    new_ids = {v['videoId'] for v in new_data}

    if new_ids != existing_ids:
        print("New content found. Updating data.json...")
        save_data(new_data)
    else:
        print("No new content. data.json is up to date.")

if __name__ == '__main__':
    scrape_and_update('UCoYAHn6JaPWFcoRSYevj9Kw')
