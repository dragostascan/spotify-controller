import cv2
import mediapipe as mp
import math
import numpy as np
import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# =================================================================
# 1. SPOTIFY AUTHENTICATION
# =================================================================
load_dotenv()

CLIENT_ID = (os.getenv("SPOTIFY_CLIENT_ID") or "").strip()
CLIENT_SECRET = (os.getenv("SPOTIFY_CLIENT_SECRET") or "").strip()
REDIRECT_URI = (os.getenv("SPOTIFY_REDIRECT_URI") or "").strip()
SCOPE = "user-modify-playback-state user-read-playback-state"

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise ValueError("Missing variables from .env")

print("Connecting to Spotify...")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))
print("Connection Successful!")

# =================================================================
# 2. INITIALISING CAMERA AND MEDIAPIPE
# =================================================================
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mp_hands.Hands(min_detection_confidence=0.7,
                      min_tracking_confidence=0.7)

vol_percent = 0
vol_bar = 400
last_vol = 0
volume_mode_active = False
cooldown = 0
volume_cooldown = 0

# =================================================================
# MAP OF GESTURES
# Format: (Thumb, Pointer, Middle, Ring, Pinky) : "COMMAND"
# True = UP, False = DOWN
# =================================================================

GESTURE_MAP = {
    (True, True, False, False, True): "TOGGLE_VOLUME",
    (False, True, True, False, False): "PLAY_PAUSE",
    (False, False, False, False, True): "NEXT_SONG",
    (True, False, False, False, False): "PREV_SONG",
    (False, False, False, False, False): "MUTE"
}

print("App is open. Press 'q' to exit!")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, c = img.shape
    RGB_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hand.process(RGB_frame)

    if cooldown > 0:
        cooldown -= 1

    if volume_cooldown > 0:
        volume_cooldown -= 1

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
            middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
            ring_up = hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y
            pinky_up = hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y
            thumb_up = hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x

            current_gesture = (thumb_up, index_up,
                               middle_up, ring_up, pinky_up)

            if current_gesture in GESTURE_MAP and cooldown == 0:
                command = GESTURE_MAP[current_gesture]

                try:

                    if command == "TOGGLE_VOLUME":
                        volume_mode_active = not volume_mode_active
                        print(
                            f"Volume Mode {'ON' if volume_mode_active else 'OFF'}")
                        cooldown = 35

                    elif not volume_mode_active:

                        if command == "PLAY_PAUSE":
                            playback = sp.current_playback()
                            if playback is not None and playback['is_playing']:
                                sp.pause_playback()
                                print("Pause")
                            else:
                                sp.start_playback()
                                print("Play")
                            cooldown = 35

                        elif command == "NEXT_SONG":
                            sp.next_track()
                            print("Next Song")
                            cooldown = 35

                        elif command == "PREV_SONG":
                            sp.previous_track()
                            print("Previous Song")
                            cooldown = 35

                        elif command == "MUTE":
                            sp.volume(0)
                            print("MUTE")
                            cooldown = 35

                except Exception as e:
                    print(
                        f"Spotify Error: Make sure Spotify is open! ({e})")
                    cooldown = 35

            if volume_mode_active:
                x1, y1 = int(
                    hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
                x2, y2 = int(
                    hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                length = math.hypot(x2 - x1, y2 - y1)

                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

                vol_percent = np.interp(length, [25, 260], [0, 100])
                vol_bar = np.interp(length, [25, 260], [400, 150])

                if length < 30:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

                # Increased threshold from 3 to 5 to ignore tiny twitches, 
                if abs(last_vol - vol_percent) > 5 and volume_cooldown == 0:
                    try:
                        sp.volume(int(vol_percent))
                        last_vol = vol_percent
                        volume_cooldown = 15  # Wait ~0.5 seconds (15 frames) before sending the next API call
                    except Exception as e:
                        pass 

                cv2.putText(img, "VOLUME MODE: ON", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(img, "VOLUME MODE: OFF", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # UI for volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol_percent)} %', (40, 450),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Spotify Controller", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
