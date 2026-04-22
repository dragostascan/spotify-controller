# Spotify Controller

A Python application that uses hand gestures captured through a webcam to control Spotify playback in real time.

## Overview

Spotify Controller is a gesture-based media control application built with Python, OpenCV, MediaPipe, and Spotipy.  
It detects the user's hand through the webcam, identifies which fingers are raised, and maps predefined gestures to Spotify commands such as:

- Play / Pause
- Next Song
- Previous Song
- Mute
- Volume Control

The project combines real-time hand tracking with Spotify Web API integration to provide an alternative, touch-free way of controlling music playback.

## Features

- Real-time hand tracking using webcam input
- Finger-state detection based on MediaPipe hand landmarks
- Gesture-to-command mapping
- Spotify playback control through Spotipy
- Separate volume control mode
- Live visual feedback with hand landmarks and volume bar
- Environment-variable based authentication using `.env`

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy
- Spotipy
- python-dotenv

## Project Structure

- `SpotifyController.py` – main application script
- `requirements.txt` – Python dependencies
- `.env.example` – example environment variables template
- `Spotify Controller.docx` – full Romanian project documentation

## Requirements

Before running the project, make sure you have:

- Python 3.11.9 installed
- Spotify desktop app installed and running
- a Spotify Developer application configured
- a valid `.env` file with your credentials

Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

## Environment Variables

Create a file named `.env` in the project folder and add:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

Important:
- do **not** upload your real `.env` file to GitHub
- make sure `.env` is listed in `.gitignore`

## Spotify API Setup

To run the application, you need to create an app in Spotify Developer Dashboard and obtain:

- Client ID
- Client Secret
- Redirect URI

Use the following redirect URI for local development:

```text
http://127.0.0.1:8888/callback
```

## How to Run

### 1. Create and activate a virtual environment

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Create the `.env` file

Add your Spotify credentials as described above.

### 4. Start Spotify

Open the Spotify desktop app and start playing a song.

### 5. Run the script

```bash
python SpotifyController.py
```

### 6. Use gestures in front of the webcam

The app will detect your hand and execute commands based on the gesture currently recognized.

## Gesture Map

The application uses the following gesture-to-command associations:

- **TOGGLE_VOLUME**
- **PLAY / PAUSE**
- **NEXT_SONG**
- **PREV_SONG**
- **MUTE**

You can customize these gestures in the `GESTURE_MAP` dictionary inside the script.

## How It Works

The application follows these main steps:

1. loads Spotify credentials from `.env`
2. authenticates with Spotify using `SpotifyOAuth`
3. opens the webcam feed
4. detects hand landmarks with MediaPipe
5. determines which fingers are raised
6. matches the detected finger pattern to a predefined gesture
7. sends the corresponding command to Spotify
8. if volume mode is active, computes the distance between thumb and index finger and maps it to a volume percentage

## Visual Feedback

The interface shows:

- webcam feed
- detected hand landmarks
- current volume mode status
- live volume bar
- current volume percentage

## Limitations

- Gesture recognition depends on lighting conditions, webcam quality, and hand positioning
- If two hands appear at the same time, gesture interpretation may become unstable
- Spotify commands require proper API authentication and a valid Spotify session
- The current gesture set is limited and may not be equally comfortable for all users

## Future Improvements

- graphical user interface
- configurable gestures
- display of the current song in the interface
- support for other media applications
- more stable gesture recognition
- mobile companion app for remote gesture-based control

## Documentation

The full Romanian-language project documentation is included in this repository as:

- `Spotify Controller.docx`
