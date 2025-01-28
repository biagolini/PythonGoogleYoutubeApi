import os
import datetime
import time
import sys
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

# Define the scopes required for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# File path to the video for upload
VIDEO_FILE_PATH = "example_video.mp4" 

# Scheduled publish timestamp in the future (Format: YYYY-MM-DDTHH:MM:SSZ)
SCHEDULED_PUBLISH_DATE = "2025-06-15T16:30:00Z" 
# 16:30 UTC corresponds to:
# 08:30 AM PST (Pacific Standard Time, UTC-8) [West Coast of the US]
# 11:30 AM EST (Eastern Standard Time, UTC-5) [New York, Miami]
# 01:30 PM BRT (Brasília Time, UTC-3) [Brazil]
# 04:30 PM GMT (Greenwich Mean Time, UTC+0) [London]
# 05:30 PM CET (Central European Time, UTC+1) [Paris, Berlin]
# 01:30 AM the next day JST (Japan Standard Time, UTC+9) [Japan]

# Default values for video metadata
DEFAULT_TITLE = None  # If None, defaults to the file name
DEFAULT_DESCRIPTION = None  # Default description
DEFAULT_TAGS = []  # Default tags are an empty list
DEFAULT_CATEGORY_ID = "22"
# Popular category IDs:
# 1: Film & Animation
# 10: Music
# 17: Sports
# 20: Gaming
# 22: People & Blogs
# 23: Comedy
# 27: Education


def upload_video_with_progress(video_file_path, scheduled_date):
    """
    Upload a video to YouTube and schedule its publication with progress feedback.

    Args:
        video_file_path (str): The file path of the video to upload.
        scheduled_date (str): The ISO 8601 formatted timestamp for the scheduled publish date.
    """
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

    # Validate if the video file exists
    if not os.path.exists(video_file_path):
        sys.stdout.write(f"\nVideo file not found: {video_file_path}\n")
        return

    # Extract default title from file name if no title is provided
    file_name = os.path.basename(video_file_path)
    title = DEFAULT_TITLE if DEFAULT_TITLE else file_name

    try:
        # Prepare the request body for video upload
        body = {
            "snippet": {
                "title": title,
                "description": DEFAULT_DESCRIPTION,
                "tags": DEFAULT_TAGS,
                "categoryId": DEFAULT_CATEGORY_ID
            },
            "status": {
                "privacyStatus": "private",  # Video remains private until published
                "publishAt": scheduled_date
            }
        }

        # Initialize media upload with chunksize
        media = MediaFileUpload(video_file_path, chunksize=1024 * 1024, resumable=True)

        # Perform the upload
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        sys.stdout.write(f"Upload started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        sys.stdout.flush()

        # Track upload progress
        start_time = time.time()
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)  # Convert to percentage
                if progress >= 1:  # Display only after 1% progress
                    elapsed_time = time.time() - start_time
                    estimated_total_time = elapsed_time / (progress / 100)
                    estimated_remaining_time = estimated_total_time - elapsed_time
                    sys.stdout.write(
                        f"\rUpload progress: {progress}% - Estimated completion: {str(datetime.timedelta(seconds=int(estimated_remaining_time)))}"
                    )
                    sys.stdout.flush()

        video_id = response.get("id")
        sys.stdout.write(f"\nVideo uploaded successfully! Video ID: {video_id}\n")

    except googleapiclient.errors.HttpError as e:
        sys.stdout.write(f"\nAn HTTP error occurred while uploading the video: {e}\n")


def main():
    """
    Main entry point for the script.
    Validates the video file path and scheduled date, then uploads the video.
    """
    # Ensure the scheduled date is in the correct format
    try:
        datetime.datetime.fromisoformat(SCHEDULED_PUBLISH_DATE.replace("Z", "+00:00"))
    except ValueError:
        sys.stdout.write("Invalid scheduled date format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.\n")
        return

    # Call the upload function with progress tracking
    upload_video_with_progress(VIDEO_FILE_PATH, SCHEDULED_PUBLISH_DATE)


if __name__ == "__main__":
    main()
