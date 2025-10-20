# Bird Detector on Raspberry Pi with Telegram Alerts

This project uses a TensorFlow Lite model on a Raspberry Pi to detect birds from the PiCamera in real time and send alerts with bounding boxes via Telegram.

## Features

- Real-time object detection using a lightweight TFLite model
- Sends bounding box images of detected birds to Telegram
- Fully automated or manually controlled via `/start`
- Optimized for Raspberry Pi with Picamera2 and tflite-runtime

## Requirements

- Raspberry Pi 4 or later
- PiCamera2 installed and configured
- Python 3.9+
- [Telegram bot](https://core.telegram.org/bots#3-how-do-i-create-a-bot) token and chat ID

Install dependencies:
```bash
pip install -r requirements.txt
