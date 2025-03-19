# YouTube Video Information Updater

The `youtube_update_video_info.py` script is designed to update video details such as titles, descriptions, tags, and localized metadata for videos in your YouTube channel.

## Purpose
This script automates the process of updating video information using the YouTube Data API. It works with a JSON configuration file where you specify the updates for each video.

## Usage
1. **Prepare the Update Configuration:**
   - Create a file named `YouTube_Data/update_videos_info.json`.
   - Structure the file as follows:

```json
{
    "<video_id_or_url>": {
        "default": {
            "title": "New Title",
            "description": "Updated description",
            "tags": ["tag1", "tag2"]
        },
        "localizations": {
            "<language_code>": {
                "title": "Localized Title",
                "description": "Localized description"
            }
        },
        "scheduledPublishTime": "2025-03-20T16:30:00Z"
    }
}
```
2. **Run the Script:**
   Execute the script using Python:
   ```bash
   python youtube_update_video_info.py
   ```

   - The script supports both direct video IDs (e.g., `fZRimwLSQAk`) and URLs (e.g., `https://youtu.be/fZRimwLSQAk`).
   - If a video ID is invalid or not found, the script will display an appropriate message in the console.

3. **Authentication:**
   - The script requires authentication with the YouTube Data API using OAuth 2.0.
   - For detailed instructions on setting up authentication, refer to the guide available on [my Medium post](https://medium.com/@biagolini).
   - You can also review the related code in the `youtube_public_data_demo.py` file for further context.

## Notes
- Ensure the `token.json` and `client_secret.json` files are in the same directory as the script to handle authentication.
- Make sure the YouTube Data API is enabled in your Google Cloud project.
- Videos scheduled for publication must be set to `private` before they can be scheduled using `scheduledPublishTime`.

Feel free to contribute or report issues in the repository!

