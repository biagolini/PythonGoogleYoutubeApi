# Google/YouTube API Automation with Python

This repository is designed to be a resource for developers exploring the integration of the YouTube Data API with Python. It showcases a variety of Python scripts and workflows for automating tasks, including both public API interactions and authenticated operations requiring user consent.

## Project Overview

This project provides:
- Python-based examples of interacting with the YouTube Data API.
- Workflows for handling public YouTube data.
- Guidance for performing authorized actions on private accounts (e.g., managing video metadata).

The goal is to deliver clean, reusable code that developers can adapt to their own applications, offering practical examples for leveraging Google APIs in automation and development tasks.

---

## Repository Structure

```
.
├── .env                # Environment variables for configuration
├── YouTube_Data        # Folder for storing output data
├── scripts.py          # Python scripts for YouTube automation
├── requirements.txt    # List of dependencies for the project
└── client_secret.json  # Google OAuth credentials (if applicable)
```

---

## Setting Up Google API Authorization Credentials

To interact with the YouTube Data API, you need to configure appropriate credentials. The credentials depend on whether you’re accessing public data or performing actions on private accounts:

### OAuth 2.0 Authentication

OAuth 2.0 is used for operations requiring user consent, such as managing private data (e.g., editing video titles or descriptions). To use this:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and configure the OAuth consent screen.
3. Generate OAuth credentials and download the `client_secret.json` file.
4. Use the file in your project for authentication.

For more information, refer to [Google's OAuth Guide](https://developers.google.com/identity/protocols/oauth2).

### API Key Access

API keys are used for accessing publicly available data, such as fetching video information from a public YouTube channel. Generate an API key by:
1. Visiting the [Google Cloud Console](https://console.cloud.google.com/).
2. Creating a project and enabling the YouTube Data API.
3. Generating an API key.

To learn more, refer to the [YouTube API Key Documentation](https://developers.google.com/youtube/registering_an_application).

---

## Identifying a YouTube Channel ID

To work with a specific YouTube channel, you need its unique channel ID. You can find it by navigating to the channel’s page. The URL typically looks like:

```
https://www.youtube.com/channel/<CHANNEL_ID>
```

The `<CHANNEL_ID>` is the value you’ll use in API requests.

---

## Installation and Setup

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

Clone the repository to your local environment:

```bash
git clone <repository-link>
cd <repository-name>
```

### 2. Create a Virtual Environment

Set up a Python virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Upgrade pip

Ensure you’re using the latest version of pip:

```bash
pip install --upgrade pip
```

### 4. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Create Output Folder

Create the output folder for local storage of data:

```bash
mkdir YouTube_Data
```

### 6. (Optional) Install Jupyter Notebook

If you plan to experiment using Jupyter Notebook, install its dependencies:

```bash
pip install notebook ipykernel
```

### 7. (Optional) Add Virtual Environment to Jupyter

Ensure the virtual environment is recognized by Jupyter:

```bash
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```


---

## Configuring the `.env` File

To run the scripts, create a `.env` file in the project root with the following structure:

```
API_KEY=your_api_key
CLIENT_ID=your_client_id.apps.googleusercontent.com
CLIENT_SECRET=your_client_secret
```

Alternatively, save your Google OAuth credentials as `client_secret.json` in the root directory.

---

## Contributing

Contributions are welcome! Feel free to:
- Submit issues for bugs or improvements.
- Create pull requests with enhancements.
- Fork the repository to build your own solutions.

---


## License and Disclaimer

This project is open-source and available under the MIT License. You are free to copy, modify, and use the project as you wish. However, any responsibility for the use of the code is solely yours. Please use it at your own risk and discretion. 

Please use it responsibly and adhere to the [YouTube API Terms of Service](https://developers.google.com/youtube/terms).
