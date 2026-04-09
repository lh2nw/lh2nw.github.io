import cv2
import numpy as np
import threading
import time
import urllib.request
from ultralytics import YOLO

# ── Config ────────────────────────────────────────────────────────────────────
ESP32_IP = "192.168.4.1"
STREAM_URL = f"http://{ESP32_IP}/stream"
MODEL_NAME = "yolov8n.pt"  # Use 'n' for real-time speed
CONF_THRESH = 0.45
DETECT_EVERY = 2  # Only run AI every 2nd frame to keep video smooth


# ── Background Threading Class ────────────────────────────────────────────────
class ESP32Stream:
    """Constantly grabs the newest frame from the ESP32 in the background."""

    def __init__(self, url):
        self.url = url
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()  # Prevents flickering during frame copy

    def start(self):
        t = threading.Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        try:
            stream = urllib.request.urlopen(self.url, timeout=10)
            bytes_data = b''
            while not self.stopped:
                bytes_data += stream.read(2048)
                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes_data[a:b + 2]
                    bytes_data = bytes_data[b + 2:]
                    img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if img is not None:
                        with self.lock:
                            self.frame = img
        except Exception as e:
            print(f"Stream Error: {e}")

    def stop(self):
        self.stopped = True


# ── Keep your original helper functions (class_colour, draw_detections, draw_hud) here ──
# (Paste your draw_detections and draw_hud functions here so the main loop can call them)

def main():
    # ... (Keep your model loading and initial variable setup) ...
    model = YOLO(MODEL_NAME)
    names = model.names

    # ── Start the background reader ──
    estream = ESP32Stream(STREAM_URL).start()

    # Wait for the first frame to arrive
    print("Waiting for stream...")
    while estream.frame is None:
        time.sleep(0.1)

    # ── Main Loop ─────────────────────────────────────────────────────────────
    try:
        while True:
            # 1. Grab the freshest frame
            with estream.lock:
                frame = estream.frame.copy()

            # 2. Timing and FPS
            # (Insert your original FPS calculation logic here)

            # 3. Detection (with skipping)
            if detection_on and frame_idx % DETECT_EVERY == 0:
                last_results = model(frame, conf=conf_thresh, verbose=False)

            # 4. Drawing (your original style)
            if detection_on and last_results:
                obj_count = draw_detections(frame, last_results, names)

            draw_hud(frame, fps_display, obj_count, detection_on, MODEL_NAME)
            cv2.imshow("ESP32-CAM Optimized", frame)

            # 5. Keyboard logic (Keep all your keys: D, S, +, -, Q)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27): break
            # ... (Rest of your key logic) ...

    finally:
        estream.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()