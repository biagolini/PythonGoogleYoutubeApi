import os
import json
import datetime
from datetime import timezone
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def load_update_data(file_path):
    """Load update data from a JSON file."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print(f"File not found: {file_path}")
            return {}
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return {}


def extract_video_id(video_identifier):
    """Extract video ID from a direct ID or YouTube URL."""
    if video_identifier.startswith("https://youtu.be/"):
        return video_identifier.replace("https://youtu.be/", "")
    return video_identifier


def is_future_date(date_str):
    """Check if the given date is in the future."""
    try:
        scheduled_date_str = date_str.replace("Z", "+00:00")  # Explicitly add UTC offset
        scheduled_date = datetime.datetime.fromisoformat(scheduled_date_str)
        current_date = datetime.datetime.now(timezone.utc)
        return scheduled_date > current_date
    except ValueError:
        print("Invalid date format provided.")
        return False


def validate_scheduled_publish_time(update_data):
    """Validate if scheduledPublishTime, if provided, is a future date."""
    for video_info in update_data.values():
        if "scheduledPublishTime" in video_info:
            if not is_future_date(video_info["scheduledPublishTime"]):
                print("Error: scheduledPublishTime must be a future date.")
                exit(1)


def main():
    update_file_path = "YouTube_Data/update_videos_info.json"
    update_data = load_update_data(update_file_path)

    if not update_data:
        print("No update data found.")
        return

    validate_scheduled_publish_time(update_data)

    try:
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", scopes=SCOPES)
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    except Exception as e:
        print(f"Authentication error: {e}")
        return

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)

    for video_identifier, video_info in update_data.items():
        video_id = extract_video_id(video_identifier)

        try:
            video_request = youtube.videos().list(
                part="snippet,localizations,status",
                id=video_id
            )
            video_response = video_request.execute()

            if not video_response["items"]:
                print(f"Video not found: {video_id}")
                continue
        except googleapiclient.errors.HttpError as e:
            print(f"Error fetching video details for {video_id}: {e}")
            continue

        video_details = video_response["items"][0]
        update_snippet = {}

        try:
            if "default" in video_info:
                default_info = video_info["default"]
                update_snippet["title"] = default_info.get("title")
                update_snippet["description"] = default_info.get("description")
                update_snippet["tags"] = default_info.get("tags")
                update_snippet["defaultLanguage"] = "en"
                update_snippet["categoryId"] = "10"  # Categoria 10 (Música)
        except Exception as e:
            print(f"Error updating snippet for {video_id}: {e}")

        update_localizations = {}
        try:
            if "localizations" in video_info:
                for lang, localization in video_info["localizations"].items():
                    update_localizations[lang] = {
                        "title": localization.get("title"),
                        "description": localization.get("description")
                    }
        except Exception as e:
            print(f"Error updating localizations for {video_id}: {e}")

        update_status = {}
        try:
            if "scheduledPublishTime" in video_info:
                update_status["publishAt"] = video_info["scheduledPublishTime"]
                update_status["privacyStatus"] = "private"
        except Exception as e:
            print(f"Error updating status for {video_id}: {e}")

        body = {}
        if update_snippet:
            body["snippet"] = update_snippet
        if update_localizations:
            body["localizations"] = update_localizations
        if update_status:
            body["status"] = update_status

        if body:
            body["id"] = video_id
            try:
                print(f"Sending update request for video {video_id}.")
                youtube.videos().update(
                    part="snippet,localizations,status",
                    body=body
                ).execute()
                print(f"Video updated successfully: {video_id}")
            except googleapiclient.errors.HttpError as e:
                print(f"An HTTP error occurred while updating video {video_id}: {e}")
                print(f"Details: {e}")
            except Exception as e:
                print(f"Unexpected error updating video {video_id}: {e}")
        else:
            print(f"No data to update for video: {video_id}")

if __name__ == "__main__":
    main()