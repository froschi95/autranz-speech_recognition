from flask import Flask, request, jsonify, render_template, redirect
import requests
import os
# import tempfile
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    transcribed_text = ''
    # Get the audio file from the request
    if "file" not in request.files:
        return redirect(request.url)
    
    audio_file = request.files['file']
    print(audio_file)
    if audio_file.filename == '':
        return redirect(request.url)
    
    if audio_file:   
    # Load the audio file
        r = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)

        # Transcribe the audio
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error while transcribing: {e}"
        transcribed_text = text
    return render_template('index.html', transcript=transcribed_text)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
