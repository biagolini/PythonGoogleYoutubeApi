import os
import json
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

# Define the scopes required for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

max_results=25

def main():
    # Check if credentials exist
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
    else:
        # Run OAuth flow to get new credentials
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        # Save credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Build the YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    try:
        # Get channel's uploads playlist ID
        channel_request = youtube.channels().list(
            part="contentDetails",
            mine=True
        )
        channel_response = channel_request.execute()
        uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        # Get the lastest videos from the uploads playlist
        videos_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        )
        videos_response = videos_request.execute()

        videos_data = {}
        for item in videos_response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]

            # Get detailed video information, including localized details
            video_request = youtube.videos().list(
                part="snippet,contentDetails,statistics,topicDetails,localizations",
                id=video_id
            )
            video_response = video_request.execute()

            if not video_response["items"]:
                continue  # Skip if no details are found

            video_details = video_response["items"][0]
            localized_titles = {}

            # Handle localized titles and descriptions
            if "localizations" in video_details:
                for lang, localization in video_details["localizations"].items():
                    localized_titles[lang] = {
                        "title": localization.get("title", ""),
                        "description": localization.get("description", "")
                    }

            # Add video data to the JSON structure
            videos_data[video_id] = {
                "default": {
                    "title": video_details["snippet"].get("title", ""),
                    "description": video_details["snippet"].get("description", ""),
                    "publishedAt": video_details["snippet"].get("publishedAt", ""),
                    "tags": video_details["snippet"].get("tags", []),
                    "channelTitle": video_details["snippet"].get("channelTitle", "")
                },
                "statistics": video_details.get("statistics", {}),
                "contentDetails": video_details.get("contentDetails", {}),
                "topicDetails": video_details.get("topicDetails", {}),
                "localizations": localized_titles
            }

        # Save the JSON data to a file
        os.makedirs("YouTube_Data", exist_ok=True)
        output_path = os.path.join("YouTube_Data", "lastest_videos_detailed.json")
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(videos_data, json_file, ensure_ascii=False, indent=4)

        print(f"Data saved to {output_path}")

    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error occurred: {e}")

if __name__ == "__main__":
    main()
