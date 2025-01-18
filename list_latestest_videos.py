import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Authentication configurations and variables
API_KEY = os.getenv('API_KEY')

def get_latest_videos(api_key, channel_id):
    # Build the YouTube API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Retrieve the uploads playlist ID
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Get the last 20 videos from the uploads playlist
    playlist_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=20
    ).execute()

    # Print basic information about the videos
    print("Latest 20 videos from the channel:")
    for item in playlist_response['items']:
        video_title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        publish_date = item['snippet']['publishedAt']
        print(f"Title: {video_title}")
        print(f"Video ID: {video_id}")
        print(f"Published Date: {publish_date}")
        print("-" * 40)

if __name__ == "__main__":
    # Replace with your YouTube channel ID
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    
    if not API_KEY or not CHANNEL_ID:
        print("Make sure to set API_KEY and CHANNEL_ID in the .env file")
    else:
        get_latest_videos(API_KEY, CHANNEL_ID)
