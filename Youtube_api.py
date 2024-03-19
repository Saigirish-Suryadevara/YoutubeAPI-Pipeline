import googleapiclient.discovery
import pandas as pd
from googleapiclient.discovery import build


def fetch_and_save_youtube_comments(): 

    api_key = 'AIzaSyCAPelAuaDMZ3EEg5BtmO-UD5uNF2G86jM'  # Your API key

        # Build the YouTube API service
    youtube = build('youtube', 'v3', developerKey=api_key)

        # Create lists to store comment data
    comment_thread_ids = []
    author_display_names = []
    comment_texts = []
    like_counts = []

        # Create a request to retrieve comment threads for a specific video
    request = youtube.commentThreads().list(
            part='id,snippet,replies',  # Parts to include in the response
            videoId='cV5TjZCJkuA'        # ID of the video
        )

        # Execute the request and get the response
    response = request.execute()

        # Function to parse comment data and append it to lists
    def parse_comment_data(comment):
            comment_thread_ids.append(comment['id'])
            snippet = comment['snippet']['topLevelComment']['snippet']
            author_display_names.append(snippet['authorDisplayName'])
            comment_texts.append(snippet['textDisplay'])
            like_counts.append(snippet['likeCount'])

        # Parse the initial response
    for item in response['items']:
            parse_comment_data(item)

        # Loop through additional pages if available
    while response.get('nextPageToken', None):
            request = youtube.commentThreads().list(
                part='id,replies,snippet',                        # Parts to include
                videoId='cV5TjZCJkuA',                            # ID of the video
                pageToken=response['nextPageToken']              # Next page token
            )
            response = request.execute()
            for item in response['items']:
                parse_comment_data(item)

        # Create a DataFrame from the parsed data
    comments_df = pd.DataFrame({
            'Comment Thread ID': comment_thread_ids,
            'Author Display Name': author_display_names,
            'Comment Text': comment_texts,
            'Like Count': like_counts
        })

        # Save the DataFrame to a CSV file
    comments_df.to_csv('youtube_comments.csv', index=False)

    print("CSV file has been created successfully!")
        
fetch_and_save_youtube_comments()
