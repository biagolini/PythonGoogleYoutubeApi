import os
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

# Define the scopes required for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

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
        # Request information about the authenticated user's channel
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        print(response)
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error occurred: {e}")

if __name__ == "__main__":
    main()