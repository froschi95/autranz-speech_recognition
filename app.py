from flask import Flask, request, jsonify, render_template, redirect
import requests
import os

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
    if audio_file.filename == '':
        return redirect(request.url)
    
    if audio_file:
        # Set the API endpoint and your API key
        api_endpoint = 'https://api.assemblyai.com/v2/transcript'
        api_key = os.getenv("API_KEY")
        
        # Set the headers for the request
        headers = {
            'Content-Type': 'audio/wav',
            'Authorization': f'Token {api_key}'
        }
        
        # Send the POST request to the AssemblyAI API
        response = requests.post(api_endpoint, headers=headers, data=audio_file)
        
        # Get the transcribed text from the response
        transcribed_text = response.json()['text']
    
    # Return the transcribed text as a response
    # return jsonify({'transcribed_text': transcribed_text})
    return render_template('index.html', transcript=transcribed_text)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
