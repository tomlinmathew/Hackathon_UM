import speech_recognition as sr
import os
import random
import pyaudio
from pydub import audio_segment
from pydub.playback import play
import pyttsx3
from flask import Flask, render_template, jsonify , flash



app = Flask(__name__)
app.secret_key = "super secret key"


# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
ai_number = 0

@app.route('/')
def index():
    return render_template('generate.html')

# Function to generate a random number for AI-generated voice

def generate_random_number():
    return random.randint(1, 10000)

#def ai_voice2(number):
    #flash(f"7 please say {number}")  

# Function to generate AI-generated voice
def ai_voice(number):
    engine.setProperty('rate', 200)
    engine.say(f"Your number is {number}")
    print(f"blaaaaaaa")
    flash(f"2 please say {number}", "success")
    #engine.runAndWait()
    print(f"2 Your number is {number}")
    # Stop the engine
    

# Function to recognize human voice
def recognize_human_voice():
    print("here")
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)
        #play(audio)

        try:
            text = r.recognize_google(audio)
            print(f"error tomlin is ", text)
            return text
        
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Function to compare human voice with AI-generated voice
def compare_voices(human_text, ai_number):
    if human_text.lower() == f"your number is {ai_number}":
        return True
    else:
        return False
@app.route('/generate', methods=['GET', 'POST'])
def generate():
    # Generate a random number for AI-generated voice
    ai_number = generate_random_number()
    print(f"1 Your number is {ai_number}")

    # Generate AI-generated voice
    ai_voice(ai_number)
    print(f"4 Your number is {ai_number}")
    return render_template('generate.html')

@app.route('/voicetest', methods=['GET', 'POST'])
#def voicetest2():
def voicetest():

    # Recognize human voice
    human_text = recognize_human_voice()
    print(f"5 Your number is {human_text}")

    # Check if the voice is AI-generated and reject it
    if human_text and not compare_voices(human_text, ai_number):
        flash("Login successful!", 'success')
        #flash(human_text)
        return render_template('test.html')
    else:
        flash("Login failed! No Human voice detected.")
        #flash(human_text)
        
    
    engine.stop()
    return render_template('generate.html')
if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))