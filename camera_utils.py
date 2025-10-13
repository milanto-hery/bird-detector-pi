import cv2

def find_available_camera(max_devices=5):
    """
    Search for an available camera index.
    Returns the first available index or -1 if none found.
    """
    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            cap.release()
            return i
    return -1

def get_camera_stream(index=None, width=640, height=480):
    """
    Initialize a camera stream at a given index or auto-detect if None.
    Returns the cv2.VideoCapture object or raises an error if not available.
    """
    if index is None:
        index = find_available_camera()
        if index == -1:
            raise IOError("❌ No camera detected.")

    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise IOError(f"❌ Failed to open camera at index {index}.")

    # Optional: set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    print(f"✅ Camera initialized at index {index} ({width}x{height})")
    return cap
