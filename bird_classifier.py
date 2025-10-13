import cv2
import numpy as np
import time
import os
from datetime import datetime
from picamera2 import Picamera2
from tflite_runtime.interpreter import Interpreter
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID

# === CONFIG ===
MODEL_PATH = 'model.tflite'
OUTPUT_DIR = 'output'
DETECTION_THRESHOLD = 0.5

LABELS = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus",
    "train", "truck", "boat", "traffic light", "fire hydrant",
    "stop sign", "parking meter", "bench", "bird", "cat", "dog",
    "horse", "sheep", "cow"
]
CLASS_BIRD = 15  # 'bird' index in COCO labels

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Init Telegram
bot = Bot(token=TELEGRAM_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ Bird detector started (Pi camera).")

# Init TFLite model
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_height = input_details[0]['shape'][1]
input_width = input_details[0]['shape'][2]

# Init PiCamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(1)

def detect_bird(frame):
    input_tensor = cv2.resize(frame, (input_width, input_height))
    input_tensor = np.expand_dims(input_tensor, axis=0).astype(np.uint8)
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]

    bird_detected = False
    for i in range(len(scores)):
        cls = int(classes[i])
        score = scores[i]
        if cls == CLASS_BIRD and score > DETECTION_THRESHOLD:
            bird_detected = True
            print(f"[INFO] 🐦 Bird detected with {score:.2f} confidence")
            ymin, xmin, ymax, xmax = boxes[i]
            h, w = frame.shape[:2]
            (xmin, xmax) = (int(xmin * w), int(xmax * w))
            (ymin, ymax) = (int(ymin * h), int(ymax * h))
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(frame, f"Bird {int(score*100)}%", (xmin, ymin - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return bird_detected, frame

# Main loop
try:
    while True:
        frame = picam2.capture_array()
        detected, annotated = detect_bird(frame)

        #cv2.imshow("Live Preview", annotated)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
            

        if os.environ.get('DISPLAY'):
            cv2.imshow("Live Preview", annotated)
            cv2.waitKey(1)


        if detected:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            filename = os.path.join(OUTPUT_DIR, f"bird_{timestamp}.jpg")
            cv2.imwrite(filename, annotated)

            msg = f"🐦 Bird detected at {timestamp}"
            bot.send_message(chat_id=CHAT_ID, text=msg)
            with open(filename, "rb") as img:
                bot.send_photo(chat_id=CHAT_ID, photo=img)

            print(f"[INFO] Photo sent: {filename}")
            time.sleep(10)

        time.sleep(1)

finally:
    picam2.stop()
    cv2.destroyAllWindows()
