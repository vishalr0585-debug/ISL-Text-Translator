# from flask import Flask, Response, render_template_string, jsonify
# import cv2
# import mediapipe as mp
# import numpy as np
# import pickle
# import pyttsx3
# import threading  # Import threading

# app = Flask(__name__)

# # Load the trained model
# model_dict = pickle.load(open('./model.p', 'rb'))
# model = model_dict['model']

# # Initialize MediaPipe
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# # Define label dictionary
# labels_dict = {
#     0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9'
# }

# output_text = ""  # Initialize output text for displaying predictions
# previous_text = ""  # Initialize previous text for speech synthesis

# # Initialize pyttsx3 engine
# engine = pyttsx3.init()

# def text_to_speech(text):
#     """Function to handle text-to-speech in a separate thread."""
#     engine = pyttsx3.init()  # Reinitialize the TTS engine for each call
#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()  # Ensure the engine is stopped after speaking


# # def generate_frames():
# #     global output_text, previous_text
# #     cap = cv2.VideoCapture(0)
# #     try:
# #         while True:
# #             ret, frame = cap.read()
# #             if not ret:
# #                 break

# #             H, W, _ = frame.shape
# #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             results = hands.process(frame_rgb)

# #             if results.multi_hand_landmarks:
# #                 for hand_landmarks in results.multi_hand_landmarks:
# #                     mp_drawing.draw_landmarks(
# #                         frame,
# #                         hand_landmarks,
# #                         mp_hands.HAND_CONNECTIONS,
# #                         mp_drawing_styles.get_default_hand_landmarks_style(),
# #                         mp_drawing_styles.get_default_hand_connections_style()
# #                     )

# #                     # Process landmarks to get features for model prediction
# #                     x_ = [landmark.x for landmark in hand_landmarks.landmark]
# #                     y_ = [landmark.y for landmark in hand_landmarks.landmark]
# #                     data_aux = [(x - min(x_), y - min(y_)) for x, y in zip(x_, y_)]

# #                     # Ensure the number of features matches the model's expectation
# #                     if len(data_aux) != 21:
# #                         continue

# #                     data_aux = np.array(data_aux).flatten().tolist()

# #                     # Predict gesture
# #                     try:
# #                         prediction = model.predict([data_aux])
# #                         predicted_character = labels_dict[int(prediction[0])]
# #                         output_text = predicted_character  # Update global output_text

# #                         # Check if the output text has changed for speech synthesis
# #                         if output_text != previous_text:
# #                             previous_text = output_text  # Update previous_text

# #                             # Start TTS in a separate thread to avoid blocking
# #                             threading.Thread(target=text_to_speech, args=(output_text,)).start()

# #                     except Exception as e:
# #                         print(f"Error during prediction: {e}")

# #             ret, buffer = cv2.imencode('.jpg', frame)
# #             frame = buffer.tobytes()
# #             yield (b'--frame\r\n'
# #                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
# #     except Exception as e:
# #         print(f"Error occurred: {e}")
# #     finally:
# #         cap.release()
# #         cv2.destroyAllWindows()

# # Add this global variable to keep track of the TTS thread
# tts_thread = None

# def generate_frames():
#     global output_text, previous_text, tts_thread
#     cap = cv2.VideoCapture(0)
#     try:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             H, W, _ = frame.shape
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = hands.process(frame_rgb)

#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     mp_drawing.draw_landmarks(
#                         frame,
#                         hand_landmarks,
#                         mp_hands.HAND_CONNECTIONS,
#                         mp_drawing_styles.get_default_hand_landmarks_style(),
#                         mp_drawing_styles.get_default_hand_connections_style()
#                     )

#                     # Process landmarks to get features for model prediction
#                     x_ = [landmark.x for landmark in hand_landmarks.landmark]
#                     y_ = [landmark.y for landmark in hand_landmarks.landmark]
#                     data_aux = [(x - min(x_), y - min(y_)) for x, y in zip(x_, y_)]

#                     # Ensure the number of features matches the model's expectation
#                     if len(data_aux) != 21:
#                         continue

#                     data_aux = np.array(data_aux).flatten().tolist()

#                     # Predict gesture
#                     try:
#                         prediction = model.predict([data_aux])
#                         predicted_character = labels_dict[int(prediction[0])]
#                         output_text = predicted_character  # Update global output_text

#                         # Check if the output text has changed for speech synthesis
#                         if output_text != previous_text:
#                             previous_text = output_text  # Update previous_text

#                             # Start TTS in a separate thread only if the previous thread is not alive
#                             if tts_thread is None or not tts_thread.is_alive():
#                                 tts_thread = threading.Thread(target=text_to_speech, args=(output_text,))
#                                 tts_thread.start()

#                     except Exception as e:
#                         print(f"Error during prediction: {e}")

#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     except Exception as e:
#         print(f"Error occurred: {e}")
#     finally:
#         cap.release()
#         cv2.destroyAllWindows()


# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/get_prediction')
# def get_prediction():
#     global output_text
#     return jsonify({'prediction': output_text})

# @app.route('/')
# def index():
#     return render_template_string('''
#          <!doctype html>
# <html lang="en">
# <head>
#     <title>Real-Time Hand Gesture Recognition</title>
#     <style>
#         /* Reset Styles */
#         * {
#             box-sizing: border-box;
#             margin: 0;
#             padding: 0;
#         }

#         /* Body Styles */
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             justify-content: center;
#             height: 100vh;
#             color: #fff;
#             overflow: hidden;
#         }

#         /* Title Styles */
#         h1 {
#             font-size: 4em;
#             margin-bottom: 20px;
#             text-align: center;
#             color: #ffffff;
#             background: linear-gradient(90deg, rgba(255, 0, 150, 1) 0%, rgba(0, 204, 255, 1) 100%);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             animation: gradientMove 3s ease-in-out infinite;
#         }

#         @keyframes gradientMove {
#             0%, 100% {
#                 background-position: 0% 50%;
#             }
#             50% {
#                 background-position: 100% 50%;
#             }
#         }

#         /* Button Container */
#         .btn-container {
#             display: flex;
#             justify-content: center;
#             margin-top: 30px;
#             width: 100%;
#         }

#         /* Button Styles */
#         button {
#             background: linear-gradient(45deg, #ff416c, #ff4b2b);
#             border: none;
#             border-radius: 50px;
#             padding: 15px 30px;
#             color: #fff;
#             font-size: 1.5em;
#             cursor: pointer;
#             transition: all 0.4s ease-in-out;
#             box-shadow: 0 8px 16px rgba(255, 75, 43, 0.6);
#             animation: buttonGlow 2s infinite alternate;
#         }

#         @keyframes buttonGlow {
#             from {
#                 box-shadow: 0 8px 16px rgba(255, 75, 43, 0.6), 0 0 20px rgba(255, 75, 43, 0.6);
#             }
#             to {
#                 box-shadow: 0 8px 16px rgba(255, 75, 43, 0.6), 0 0 40px rgba(255, 75, 43, 1);
#             }
#         }

#         button:hover {
#             transform: translateY(-5px) scale(1.05);
#             background: linear-gradient(45deg, #ff4b2b, #ff416c);
#         }

#         button:active {
#             transform: scale(0.98);
#             box-shadow: 0 6px 12px rgba(255, 75, 43, 0.5);
#         }

#         /* Video Container Styles */
#         #video-container {
#             display: none;
#             margin-top: 40px;
#             text-align: center;
#             animation: fadeIn 2s;
#         }

#         @keyframes fadeIn {
#             from {
#                 opacity: 0;
#             }
#             to {
#                 opacity: 1;
#             }
#         }

#         /* Video Feed Styles */
#         #video-feed {
#             width: 640px;
#             height: 480px;
#             border: 10px solid #ff416c;
#             border-radius: 20px;
#             box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
#             animation: pulse 2s infinite alternate;
#         }

#         @keyframes pulse {
#             from {
#                 transform: scale(1);
#                 box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
#             }
#             to {
#                 transform: scale(1.02);
#                 box-shadow: 0 10px 20px rgba(0, 0, 0, 0.8);
#             }
#         }

#         /* Prediction Output Box */
#         #output-box {
#             width: 100%;
#             text-align: center;
#             margin-top: 20px;
#             font-size: 2em;
#             padding: 15px;
#             background: rgba(0, 0, 0, 0.7);
#             border-radius: 15px;
#             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
#             animation: fadeIn 2s;
#         }

#         /* Media Queries */
#         @media screen and (max-width: 768px) {
#             h1 {
#                 font-size: 2.5em;
#             }

#             button {
#                 font-size: 1.2em;
#                 padding: 12px 24px;
#             }

#             #video-feed {
#                 width: 90%;
#                 height: auto;
#             }

#             #output-box {
#                 font-size: 1.5em;
#             }
#         }
#     </style>
#     <script>
#         function startVideo() {
#             document.getElementById('video-container').style.display = 'block';
#             setInterval(function() {
#                 fetch('/get_prediction')
#                     .then(response => response.json())
#                     .then(data => {
#                         document.getElementById('output-box').innerText = 'Prediction: ' + data.prediction;
#                     })
#                     .catch(error => console.error('Error fetching prediction:', error));
#             }, 500);
#         }
#     </script>
# </head>
# <body>
#     <h1>Real-Time Hand Gesture Recognition</h1>
#     <div class="btn-container">
#         <button onclick="startVideo()">Start Video</button>
#     </div>
#     <div id="video-container">
#         <img src="{{ url_for('video_feed') }}" id="video-feed">
#         <div id="output-box"></div>
#     </div>
# </body>
# </html>
#     ''')

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, Response, render_template_string, jsonify
import cv2
import mediapipe as mp
import numpy as np
import pickle
import threading
import pyttsx3

app = Flask(__name__)

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Define label dictionary
labels_dict = {
    0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9'
}

output_text = ""  # Initialize output text for displaying predictions
previous_text = ""  # Initialize previous text for speech synthesis
tts_lock = threading.Lock()  # Lock to manage TTS synchronization

# Initialize TTS engine
# tts_engine = pyttsx3.init()
# engine = pyttsx3.init()  # Reinitialize the TTS engine for each call

def text_to_speech(text):
    """Function to handle text-to-speech in a separate thread."""
    tts_engine = pyttsx3.init()
    tts_engine.say(text)
    tts_engine.runAndWait()
    tts_engine.stop()  # Ensure the engine is stopped after speaking

def generate_frames():
    global output_text, previous_text
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            H, W, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    # Process landmarks to get features for model prediction
                    x_ = [landmark.x for landmark in hand_landmarks.landmark]
                    y_ = [landmark.y for landmark in hand_landmarks.landmark]
                    data_aux = [(x - min(x_), y - min(y_)) for x, y in zip(x_, y_)]

                    # Ensure the number of features matches the model's expectation
                    if len(data_aux) != 21:
                        continue

                    data_aux = np.array(data_aux).flatten().tolist()

                    # Predict gesture
                    try:
                        prediction = model.predict([data_aux])
                        predicted_character = labels_dict[int(prediction[0])]
                        output_text = predicted_character  # Update global output_text

                        # Check if the output text has changed for speech synthesis
                        if output_text != previous_text:
                            previous_text = output_text  # Update previous_text

                            # Start TTS in a separate thread
                            threading.Thread(target=text_to_speech, args=(output_text,)).start()

                    except Exception as e:
                        print(f"Error during prediction: {e}")

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_prediction')
def get_prediction():
    global output_text
    return jsonify({'prediction': output_text})

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
<html lang="en">
<head>
    <title>Real-Time Hand Gesture Recognition</title>
    <style>
        /* Reset Styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        /* Body Styles */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: #fff;
            overflow: hidden;
        }

        /* Title Styles */
        h1 {
            font-size: 4em;
            margin-bottom: 20px;
            text-align: center;
            color: #ffffff;
            background: linear-gradient(90deg, rgba(255, 0, 150, 1) 0%, rgba(0, 204, 255, 1) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientMove 3s ease-in-out infinite;
        }

        @keyframes gradientMove {
            0%, 100% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
        }

        /* Button Container */
        .btn-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
            width: 100%;
        }

        /* Button Styles */
        button {
            background: linear-gradient(45deg, #ff416c, #ff4b2b);
            border: none;
            border-radius: 50px;
            padding: 15px 30px;
            color: #fff;
            font-size: 1.5em;
            cursor: pointer;
            transition: all 0.4s ease-in-out;
            box-shadow: 0 8px 16px rgba(255, 75, 43, 0.6);
            animation: buttonGlow 2s infinite alternate;
        }

        @keyframes buttonGlow {
            from {
                box-shadow: 0 8px 16px rgba(255, 75, 43, 0.6), 0 0 20px rgba(255, 75, 43, 0.6);
            }
            to {
                box-shadow: 0 8px 16px rgba(255, 75, 43, 0.6), 0 0 40px rgba(255, 75, 43, 1);
            }
        }

        button:hover {
            transform: translateY(-5px) scale(1.05);
            background: linear-gradient(45deg, #ff4b2b, #ff416c);
        }

        button:active {
            transform: scale(0.98);
            box-shadow: 0 6px 12px rgba(255, 75, 43, 0.5);
        }

        /* Video Container Styles */
        #video-container {
            display: none;
            margin-top: 40px;
            text-align: center;
            animation: fadeIn 2s;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        /* Video Feed Styles */
        #video-feed {
            width: 640px;
            height: 480px;
            border: 10px solid #ff416c;
            border-radius: 20px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
            animation: pulse 2s infinite alternate;
        }

        @keyframes pulse {
            from {
                transform: scale(1);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
            }
            to {
                transform: scale(1.02);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.8);
            }
        }

        /* Prediction Output Box */
        #output-box {
            width: 100%;
            text-align: center;
            margin-top: 20px;
            font-size: 2em;
            padding: 15px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
            animation: fadeIn 2s;
        }

        /* Media Queries */
        @media screen and (max-width: 768px) {
            h1 {
                font-size: 2.5em;
            }

            button {
                font-size: 1.2em;
                padding: 12px 24px;
            }

            #video-feed {
                width: 100%;
                height: auto;
            }
        }

        @media screen and (max-width: 480px) {
            h1 {
                font-size: 2em;
            }

            button {
                font-size: 1em;
                padding: 10px 20px;
            }
        }
    </style>
    <script>
        function startVideo() {
            document.getElementById('video-container').style.display = 'flex';
            fetchPrediction();  // Start fetching predictions
        }

        function fetchPrediction() {
            setInterval(() => {
                fetch('/get_prediction')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('output-box').innerText = 'Prediction: ' + data.prediction;
                    })
                    .catch(error => console.error('Error fetching prediction:', error));
            }, 500);
        }
    </script>
</head>
<body>
    <h1>Real-Time Hand Gesture Recognition</h1>
    <div class="btn-container">
        <button onclick="startVideo()">Start Video</button>
    </div>
    <div id="video-container">
        <img src="{{ url_for('video_feed') }}" id="video-feed">
        <div id="output-box"></div>
    </div>
</body>
</html>
    ''')

if __name__ == "__main__":
    app.run(debug=True)
