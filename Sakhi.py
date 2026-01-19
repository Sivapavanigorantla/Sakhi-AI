import os
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3
import openai

openai.api_key=""  # Replace with your own account made OpenAI API key

engine=pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0) 
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  

def speak(text):
    print(f"Lilith: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query=recognizer.recognize_google(audio, language="en-US")
        print(f"You: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you repeat?")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None

def open_file(file_path):
    try:
        os.startfile(file_path)  # For Windows
        # os.system(f'open {file_path}')  # For macOS
        # os.system(f'xdg-open {file_path}')  # For Linux
        return f"Opened {file_path}"
    except Exception as e:
        return f"Error opening file: {e}"

def search_web(query):
    try:
        url=f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching the web for {query}"
    except Exception as e:
        return f"Error searching the web: {e}"

def get_weather(city):
    try:
        api_key="61980fe754a07180d2d2afd16a295ebf"  
        url=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response=requests.get(url)
        weather_data=response.json()
        weather=weather_data['weather'][0]['description']
        return f"The weather in {city} is {weather}"
    except Exception as e:
        return f"Error fetching weather: {e}"

def chat_with_gpt(prompt):
    try:
        response=openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Lilith."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message['content'].strip()
    except openai.error.AuthenticationError:
        return "Error: Invalid OpenAI API key. Please check your API key."
    except openai.error.RateLimitError:
        return "Error: You've exceeded your API usage limit. Please check your billing."
    except Exception as e:
        return f"Error communicating with OpenAI: {e}"

def process_query(query):
    if query is None:
        return
    elif "open file" in query:
        file_path=query.split("open file")[1].strip()
        speak(open_file(file_path))
    elif "search" in query:
        search_query=query.split("search")[1].strip()
        speak(search_web(search_query))
    elif "weather" in query:
        city=query.split("weather")[1].strip()
        speak(get_weather(city))
    elif "exit" in query or "bye" in query or "goodbye" in query:
        speak("Goodbye! Have a great day!")
        exit()
    else:
        response=chat_with_gpt(query)
        speak(response)

if __name__=="__main__":
    speak("Hello, I am Lilith. How can I assist you today?")
    while True:
        query=listen()
        process_query(query)