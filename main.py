import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display the form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/generate', methods=['POST'])
def generate():
    music_prompt = request.form.get('musicprompt')

    # Call the generate_audio.py script with the music prompt
    result = subprocess.run(
        ['python', 'generate_audio.py', music_prompt],
        capture_output=True,
        text=True
    )

    # Check if the process returned an error
    if result.returncode != 0:
        # Log the error message to the log file
        with open("audio_generation.log", "a") as log_file:
            log_file.write(f"Error: {result.stderr}\n")
        # Return a user-friendly error message without crashing the app
        return "An error occurred while generating audio. Please try again."

    # Read the log file for successful execution
    with open("audio_generation.log", "r") as log_file:
        log_contents = log_file.read()

    return f"You entered: {music_prompt}. Audio generation complete!<br><br>Logs:<br><pre>{log_contents}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
