import pyttsx3 as p
import speech_recognition as sr
import google.generativeai as genai
import webbrowser
import pywhatkit
import os



def speak(text):
    engine = p.init()
    engine.say(text)
    engine.runAndWait()

def voice_assistant(question):
    prompt = f"You are an AI voice assistant named Igris. The user asked: '{question}'. Respond accordingly."

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt])
        
    if response and response.text:
        return response.text
    else:
        return "I'm not sure how to respond to that."

def execute_command(command):
    command = command.lower()
    
    if 'open youtube' in command:
        webbrowser.open('https://www.youtube.com')
        speak('Opening YouTube.')
    elif 'play' in command:
        song = command.replace('play', '').strip()
        speak(f'Playing {song} on YouTube.')
        pywhatkit.playonyt(song)
    elif 'search in google for' in command:
        search_query = command.replace('searching in google for', '').strip()
        speak(f'Searching Google for {search_query}.')
        webbrowser.open(f'https://www.google.com/search?q={search_query}')
    elif 'open browser' in command:
        webbrowser.open('https://www.google.com')
        speak('Opening web browser.')
    elif 'open' in command:
        app_name = command.replace('open', '').strip()
        try:
            os.system(f'start {app_name}')
            speak(f'Opening {app_name}.')
        except Exception as e:
            speak(f"Sorry, I can't open {app_name}.")
    else:
        response = voice_assistant(command)
        if response is not None:
            print(f"Igris : {response}")
            speak(response)



if __name__ == "__main__":
        speak("Hello , My name is Igris, iam your assistant!,How can i help you today?")
    
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.energy_threshold = 1000  # Adjusted threshold
            r.adjust_for_ambient_noise(source, duration=1.2)
            
            while True:
                    try:
                        print("Listening...")
                        audio = r.listen(source)
                        if audio is not None:
                            print(audio)
                            command = r.recognize_google(audio)
                            print(f"User: {command}")
                            execute_command(command)
                            
                            if "stop" in command.lower() or "exit" in command.lower():
                                speak("Hope i have played my role well, bye")
                                break
                            
                    except sr.UnknownValueError:
                        print("Sorry, I did not understand that.")
                        speak("Sorry, I did not understand that.")



