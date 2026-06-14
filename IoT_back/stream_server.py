from flask import Flask, Response
from flask_cors import CORS
import cv2
from picamera2 import Picamera2
import tensorflow as tf
import numpy as np
from datetime import datetime
from scipy.special import softmax
import requests
import config
from time import sleep


app = Flask(__name__)
CORS(app)

print(f"[{datetime.now()}][STATUS] Starting prediction model...")
interpreter = tf.lite.Interpreter(model_path="robotArm.tflite", num_threads=4)
print(f"[{datetime.now()}][INFO] Obtained AI model tflite, allocating tensors...")
interpreter.allocate_tensors()
print(f"[{datetime.now()}][INFO] Tensors allocated, loading input and output details...")
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(f"[{datetime.now()}][STATUS] Starting Camera...")
capture = Picamera2()
capture.start()
print(f"[{datetime.now()}][INFO] Camera loaded successfully... preparing for input capture...")

def generate_frames():
    while True:
        array = capture.capture_array()
        if array.shape[2] == 4:
           array = array[:, :, :3]
        resized_frame = cv2.resize(array, (128, 128))
        scaled_frame = resized_frame.astype(np.float32) / 255.0
        input_data = np.expand_dims(scaled_frame, axis=0)
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        predictions_raw = interpreter.get_tensor(output_details[0]['index'])
        predictions = softmax(predictions_raw, axis=1)
        predicted_class = np.argmax(predictions[0])
        brick_name = config.BRICK_MAPPING.get(predicted_class, "Unknown Object")
        confidence = predictions[0][predicted_class] * 100
        print(f"[{datetime.now()}][PREDICTION] I think I see {brick_name} | Confidence: {confidence:.1f}%")

        if config.SENDDATA == True:
            payload = {
                "predicted_name": brick_name,
                "confidence": round(confidence, 1)
            }
            try:
                response = requests.post(config.BACKEND_URL, json=payload, timeout=1)
                print(f"[{datetime.now()}][SENT] Prediction Json sent to backend")
            except requests.exceptions.RequestException as e:
                print(f"[{datetime.now()}][WARN] Error:  Flask server is currently down, does not affect script.  Program will continue as normal. {e}")

        display_frame = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        
        display_frame = cv2.rotate(display_frame, cv2.ROTATE_180)

        display_frame = cv2.resize(display_frame, (480, 360))

        ret, buffer = cv2.imencode('.jpg', display_frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        frame_bytes = buffer.tobytes()

        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        sleep(0.05)
        
@app.route('/video-feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)






