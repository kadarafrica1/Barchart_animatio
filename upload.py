import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# FIIRO GAAR AH: Waxaan halkaan ka akhrisanaynaa Tokens-ka qarsoon ee GitHub Secrets
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

request_body = {
    'snippet': {
        'title': 'Bar Chart Race Animation Otomaatig Ah!',
        'description': 'Muqaalkan waxaa si otomaatig ah u sameeyay AI iyo GitHub Actions.',
        'tags': ['barchart', 'data', 'animation'],
        'categoryId': '28' # Science & Technology
    },
    'status': {
        'privacyStatus': 'public' # Ama 'private' si aad marka hore u hubiso
    }
}

media_file = MediaFileUpload('bar_chart_race.mp4', chunksize=-1, resumable=True)

print("Hadda waxaa bilaamay upload-ka YouTube...")
request = youtube.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=media_file
)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Boqolkiiba inta la upload gareeyay: {int(status.progress() * 100)}%")

print(f"Muqaalka si guul leh ayaa loo galiyay! Video ID: {response['id']}")
