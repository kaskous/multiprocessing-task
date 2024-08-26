# Mouse Tracker with Webcam Capture

This application captures the current mouse coordinates and, upon clicking the left mouse button, takes a picture with the connected webcam. The coordinates and the path to the captured image are saved in an SQLite database.

## How to Run

1. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Run the application:
    ```
    python app/main.py
    ```

3. Open your browser and navigate to `http://localhost:5000` to see the real-time mouse coordinates.

## Project Structure

- `app/main.py`: The main entry point to start the application.
- `app/webserver.py`: Handles the Flask web server and WebSocket communication.
- `app/serial_reader.py`: Simulates reading serial data (mouse coordinates).
- `app/camera_capture.py`: Captures webcam images when the left mouse button is clicked.
- `app/database.py`: Manages the SQLite database for storing coordinates and image paths.