import speech_recognition as sr
import webbrowser
import win32com.client
import os
from playsound import playsound
import datetime
from config import gemini_api_key
import google.generativeai as genai
import time


conversation = []

# user_history = []


def chat(prompt):
    global conversation
    conversation.append({"role" : "Darshan" , "content" : prompt})
    print(f"Role : Darshan \nContent : {prompt}")
    
    genai.configure(api_key=gemini_api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        #   "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=f"you are jarvis, a virtual assistant. you are provided with conversation history {conversation} and your work is to go through the history and analyze it. and if your input prompt is available in history then answer the input from conversation history and if the question is new to you then answer how you normally answer. answers should be to the point and short."
    )

    chat_session = model.start_chat(history = [])

    response = chat_session.send_message(prompt)
    response.resolve()
    
    conversation.append({"role" : "Jarvis","content" : response.text})
    
    if "history".lower() in prompt.lower():
        return chat_session.history
    
    if "clear conversation history".lower() in prompt.lower():
        conversation = []
    return response.text
    

def gemini_ai(prompt):
    
    genai.configure(api_key=gemini_api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        #   "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        system_instruction="Your name is David, an AI assistant. Act as a friendly, smart, supportive, guiding assistant to user. also remember the inputs of user. Keep your answer short, to the point. ",
    )

    chat = model.start_chat(history = [])

    response = chat.send_message(prompt)

    return (response.text)

def summarizer(history):
    summary = gemini_ai(f"summarize the following text : {history}")
    return summary

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    # r.adjust_for_ambient_noise = 1

    with sr.Microphone() as source:
        r.pause_threshold = 0.8

        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-us")

            return query
        except Exception as e:
            print(e)
            say("Some error occurred by Jarvis A I")


if __name__ == "__main__":
    say("Hello I am Jarvis A I")
    sites = [["Youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.org"],["google","https://google.com"]]
    while True:
        print("listening..")
        command = takeCommand()
        # print(f"Query : {command}")
        try:
            for site in sites:
                if f"open {site[0]}".lower() in command.lower():
                    say(f"opening {site[0]} Sir")
                    print(f"opening {site[0]} Sir")
                    webbrowser.open(site[1])

            if "quit" in command.lower():
                break
            
            elif "open music" in command.lower():
                musicPath = "C:/Users/acer/Downloads/sample_music.mp3"
                # playsound(musicPath) #alternate way
                os.system(f"start {musicPath}")

            elif "time" in command.lower():
                hour = datetime.datetime.now().strftime("%H")
                mins = datetime.datetime.now().strftime("%M")
                say(f"Current time is {hour} hours {mins} minutes")

            elif "search".lower() in command.lower():
                base_url = "https://www.google.com/search?q="
                search_item = command.split("search",1)[1] # splits the command once after word "search" and returns words after search
                final_search_item = str('+'.join(search_item.split())) #separates words in search_item with +
                final_url = base_url+final_search_item
                webbrowser.open_new(final_url)

            elif "artificial".lower() in command.lower():
                prompt = command.split("intelligence",1)[1]
                response = gemini_ai(prompt)
                print(response)
            
            elif "conversation history".lower() in command.lower():
                    chat_history = chat(command)
                    
            else:
                chat_response = chat(command)
                print(f"Role : Jarvis\nContent : {chat_response}")
                say(chat_response)
                
                
        except Exception as e:
            # print(e)
            pass