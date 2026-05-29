import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

client_id = os.environ.get('YT_CLIENT_ID')
client_secret = os.environ.get('YT_CLIENT_SECRET')
refresh_token = os.environ.get('YT_REFRESH_TOKEN')

creds = Credentials(
    None,
    refresh_token=refresh_token,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=client_id,
    client_secret=client_secret
)

youtube = build('youtube', 'v3', credentials=creds)

# Automated English Title and Description perfectly matching the video content
request_body = {
    'snippet': {
        'title': 'Top 10 Most Populous Countries (1960 - 2024) | Bar Chart Race',
        'description': (
            'Watch the historical population shift from 1960 to 2024. '
            'This data visualization shows the top 10 most populous countries '
            'competing over time. Fully automated using official World Bank data.'
        ),
        'tags': ['barchartrace', 'population growth', 'data visualization', 'demographics', 'top 10'],
        'categoryId': '28' # Science & Technology
    },
    'status': {
        'privacyStatus': 'public' 
    }
}

media_file = MediaFileUpload('bar_chart_race.mp4', chunksize=-1, resumable=True)

print("Uploading video to YouTube with English optimization...")
request = youtube.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=media_file
)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Upload Progress: {int(status.progress() * 100)}%")

print(f"Upload successful! Video ID: {response['id']}")
