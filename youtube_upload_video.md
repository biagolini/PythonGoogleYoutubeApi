# YouTube Video Upload Script

This script automates the process of uploading a video to YouTube using the YouTube Data API. It also schedules the video for publication at a future date.

## Variables Explained
- **SCOPES**: Defines the required OAuth permissions. The current scope (`https://www.googleapis.com/auth/youtube.force-ssl`) allows uploading and managing videos securely.
- **VIDEO_FILE_PATH**: Specifies the local file path of the video to be uploaded. Replace the placeholder with the actual file path of your video.
- **SCHEDULED_PUBLISH_DATE**: Sets the date and time for when the video should be published. The format is ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`). Ensure the time is in UTC.

## Configuring Timezones
To configure a timezone for the scheduled publish date, convert the local time to UTC. Here are some examples:
- **UTC**: `2025-02-01T12:30:00Z`
- **PST (Pacific Standard Time)**: UTC-8. For 9:30 AM PST, use `2025-02-01T17:30:00Z`.
- **EST (Eastern Standard Time)**: UTC-5. For 9:30 AM EST, use `2025-02-01T14:30:00Z`.
- **BRT (Brasília Time)**: UTC-3. For 9:30 AM BRT, use `2025-02-01T12:30:00Z`.

Use a timezone converter to ensure accuracy.

## Video Categories
Below are some popular categories:
- **1**: Film & Animation
- **10**: Music
- **17**: Sports
- **20**: Gaming
- **23**: Comedy
- **27**: Education

You can view other ouTube video category IDs 
[Here](https://www.jlexart.com/articles/youtube-video-categories-list-78ps).

## Additional Resources
For further details on the YouTube Data API and uploading videos, refer to the official documentation:
[YouTube Data API Documentation](https://developers.google.com/youtube/registering_an_application).