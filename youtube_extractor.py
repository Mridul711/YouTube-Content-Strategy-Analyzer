import pandas as pd
from googleapiclient.discovery import build

# --- CONFIGURATION ---
# 1. PASTE YOUR API KEY HERE
api_key = "YOUR_API_KEY_HERE" 

# 2. Target Channel ID (Example: CodeWithHarry)
# You can change this to any channel you want to audit
channel_id = "UCeVMnSShP_Iviwkknt83cww" 

# ---------------------

print("Step 1: Connecting to YouTube API...")
try:
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Get Channel Stats (Subscribers, Total Views)
    request = youtube.channels().list(part='statistics,snippet', id=channel_id)
    response = request.execute()
    
    if not response['items']:
        print("Error: Channel ID not found.")
        exit()
        
    title = response['items'][0]['snippet']['title']
    subs = response['items'][0]['statistics']['subscriberCount']
    print(f"Success! Connected to channel: {title} ({subs} Subscribers)")
    
    # Get Uploads Playlist ID (This is where all videos live)
    content_details = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    uploads_playlist_id = content_details['items'][0]['contentDetails']['relatedPlaylists']['uploads']

except Exception as e:
    print(f"API Error: {e}")
    print("Did you enable 'YouTube Data API v3' in Google Cloud?")
    exit()

print("Step 2: Fetching Video Data (This is fast!)...")

videos = []
next_page_token = None

# Loop to get 50 videos (You can increase this)
while len(videos) < 50:
    playlist_request = youtube.playlistItems().list(
        part='snippet',
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )
    playlist_response = playlist_request.execute()

    # Get Video IDs to fetch deep stats (Views, Likes)
    vid_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_response['items']]
    
    # Batch request for video statistics
    stats_request = youtube.videos().list(
        part="statistics,contentDetails",
        id=','.join(vid_ids)
    )
    stats_response = stats_request.execute()

    # Combine Data
    for stat_item, playlist_item in zip(stats_response['items'], playlist_response['items']):
        title = playlist_item['snippet']['title']
        published_at = playlist_item['snippet']['publishedAt']
        
        # Stats might be hidden/missing, so we use .get()
        view_count = int(stat_item['statistics'].get('viewCount', 0))
        like_count = int(stat_item['statistics'].get('likeCount', 0))
        comment_count = int(stat_item['statistics'].get('commentCount', 0))
        
        # Duration is returned as "PT10M30S" (ISO 8601 format)
        duration_iso = stat_item['contentDetails']['duration']

        videos.append({
            'Title': title,
            'Views': view_count,
            'Likes': like_count,
            'Comments': comment_count,
            'Date': published_at,
            'Duration_ISO': duration_iso
        })
    
    next_page_token = playlist_response.get('nextPageToken')
    if not next_page_token:
        break

print(f"Step 3: Saving {len(videos)} videos to CSV...")
df = pd.DataFrame(videos)
df.to_csv('youtube_data.csv', index=False)
print(df.head())
print("Done! File saved as 'youtube_data.csv'")
