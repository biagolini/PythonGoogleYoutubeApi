import os
import json
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

# Define the scopes required for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def load_update_data(file_path):
    """Load update data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        print(f"File not found: {file_path}")
        return {}


def extract_video_id(video_identifier):
    """Extract video ID from a direct ID or YouTube URL."""
    if video_identifier.startswith("https://youtu.be/"):
        return video_identifier.replace("https://youtu.be/", "")
    return video_identifier


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

    # Load update data
    update_file_path = "YouTube_Data/update_videos_info.json"
    update_data = load_update_data(update_file_path)

    if not update_data:
        print("No update data found.")
        return

    for video_identifier, video_info in update_data.items():
        video_id = extract_video_id(video_identifier)
        try:
            # Check if the video exists
            video_request = youtube.videos().list(
                part="snippet,localizations",
                id=video_id
            )
            video_response = video_request.execute()

            if not video_response["items"]:
                print(f"Video not found: {video_id}")
                continue

            # Prepare updated data
            video_details = video_response["items"][0]
            update_snippet = video_details.get("snippet", {})
            update_localizations = video_details.get("localizations", {})

            # Update title, description, and tags if provided
            if "default" in video_info:
                default_info = video_info["default"]
                update_snippet["title"] = default_info.get("title", update_snippet.get("title"))
                update_snippet["description"] = default_info.get("description", update_snippet.get("description"))
                update_snippet["tags"] = default_info.get("tags", update_snippet.get("tags"))
                update_snippet["defaultLanguage"] = "en"  # Define the default language

            # Update localizations if provided
            if "localizations" in video_info:
                for lang, localization in video_info["localizations"].items():
                    update_localizations[lang] = {
                        "title": localization.get("title", update_localizations.get(lang, {}).get("title", "")),
                        "description": localization.get("description", update_localizations.get(lang, {}).get("description", ""))
                    }

            # Perform the update
            youtube.videos().update(
                part="snippet,localizations",
                body={
                    "id": video_id,
                    "snippet": update_snippet,
                    "localizations": update_localizations
                }
            ).execute()

            print(f"Video updated successfully: {video_id}")

        except googleapiclient.errors.HttpError as e:
            print(f"An HTTP error occurred while updating video {video_id}: {e}")


if __name__ == "__main__":
    main()
