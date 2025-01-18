# Google/YouTube API with Python

This project serves as an educational resource for developers interested in learning how to interact with the YouTube Data API. Through Python-based examples, it provides insights into handling both public data and performing authorized actions on your own account, such as editing video metadata.

## Project Overview

The repository is structured to showcase examples of both public API interactions and authenticated operations requiring user consent. The project emphasizes clean, reusable code and practical workflows for integrating Google APIs into your applications.

## Project Structure

```
.
├── .env                # Environment variables
├── scripts/            # Directory for Python scripts
├── requirements.txt    # List of Python dependencies
```

## Google API Authorization Credentials

To access the YouTube Data API, you need to configure appropriate credentials. The type of credentials depends on your use case:

### OAuth 2.0

Use OAuth 2.0 credentials when your application needs access to private user data. Your application sends a client ID and potentially a client secret to obtain an OAuth token. These credentials support scenarios like editing your YouTube video titles or descriptions.

- **How to Set Up**: Visit the [Google Cloud Console](https://console.cloud.google.com/), create a project, and configure an OAuth consent screen along with credentials.
- **Recommended Tutorial**: [YouTube Data API Authorization Guide](https://www.youtube.com/watch?v=th5_9woFJmk)

### API Keys

Use API keys for accessing public data without the need for user authentication. API keys are project-specific and can be generated in the Google Cloud Console.

- **Learn More**: [YouTube API Key Documentation](https://developers.google.com/youtube/registering_an_application)

## Identifying a YouTube Channel ID

To work with specific channels, you need the channel’s unique ID. You can find this by navigating to the desired YouTube channel and inspecting its URL, which will look like:

```
https://www.youtube.com/channel/<CHANNEL_ID>
```

## Installation and Setup

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository-link>
cd <repository-name>
```

### 2. Set Up a Virtual Environment

Create and activate a Python virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Update pip

Ensure you’re using the latest version of pip:

```bash
pip install --upgrade pip
```

### 4. Install Dependencies

Install the required libraries listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. (Optional) Jupyter Notebook Setup

If you plan to experiment or develop using Jupyter Notebook, install the necessary dependencies:

```bash
pip install notebook ipykernel
```

### Configuring the `.env` File

To run the project, you need to configure a `.env` file with the following structure:

```
API_KEY=xxxx
CLIENT_ID=xxxx.apps.googleusercontent.com
CLIENT_SECRET=xxxx
```

Replace `xxxx` with your actual API key, client ID, and client secret obtained from the Google Cloud Console.

## Contributing

Feel free to submit issues, create pull requests, or fork the repository to help improve the project.

## License and Disclaimer

This project is open-source and available under the MIT License. You are free to copy, modify, and use the project as you wish. However, any responsibility for the use of the code is solely yours. Please use it at your own risk and discretion.
