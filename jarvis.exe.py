import datetime
import webbrowser
import wikipedia
import pywhatkit
import os
import psutil
import pyjokes
import requests
import pyttsx3

# Initialize pyttsx3 (text-to-speech)
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. How can I help you today?")

# === Self-update feature ===
UPDATE_URL = "https://your-download-link.com/jarvis.py"  # Replace with your actual hosted file URL

def check_for_updates():
    try:
        print("Checking for updates...")
        response = requests.get(UPDATE_URL)
        if response.status_code == 200:
            new_code = response.text
            local_file = os.path.realpath(__file__)
            with open(local_file, "r", encoding="utf-8") as f:
                current_code = f.read()

            if new_code != current_code:
                speak("An update is available. Updating now.")
                with open(local_file, "w", encoding="utf-8") as f:
                    f.write(new_code)
                speak("Update complete. Please restart Jarvis.")
                exit()
            else:
                speak("Jarvis is up to date.")
        else:
            speak("Could not connect to update server.")
    except Exception as e:
        speak(f"Update check failed: {str(e)}")

# === Main function ===
def main():
    check_for_updates()
    wish_user()

    while True:
        query = input("You: ").lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            result = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
            speak(result)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'play' in query:
            song = query.replace('play', '')
            speak(f'Playing {song}')
            pywhatkit.playonyt(song)

        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"Current time is {time}")

        elif 'battery' in query:
            battery = psutil.sensors_battery()
            speak(f"Battery is at {battery.percent} percent")

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't understand that.")

# === Run Jarvis ===
if __name__ == "__main__":
    main()
