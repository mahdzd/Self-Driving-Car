
import cv2
import numpy as np
import subprocess

WIDTH = 640
HEIGHT = 480

# Run libcamera-vid in the background and pipe MJPEG output
command = [
    'libcamera-vid',
    '-t', '0',
    '--inline',
    '--width', str(WIDTH),
    '--height', str(HEIGHT),
    '--framerate', '30',
    '--codec', 'mjpeg',
    '-o', '-'
]

process = subprocess.Popen(command, stdout=subprocess.PIPE)

while True:
    # Read MJPEG bytes from libcamera-vid output
    jpeg_data = b''
    while True:
        chunk = process.stdout.read(1024)
        if not chunk:
            break
        jpeg_data += chunk
        if b'\xff\xd9' in chunk:
            break

    frame = cv2.imdecode(np.frombuffer(jpeg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    if frame is not None:
        cv2.imshow("Camera View", frame)

    if cv2.waitKey(1) == ord('q'):
        break

process.terminate()
cv2.destroyAllWindows()

