import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management (flashing messages)

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
        # Flash an error message and redirect to the home page
        flash("An error occurred while generating audio. Please try again.", "error")
        return redirect(url_for('index'))

    # Flash a success message and redirect to the home page
    flash("Audio generation complete! Check the audio_output directory.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
