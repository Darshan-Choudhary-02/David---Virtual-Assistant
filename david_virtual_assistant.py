import speech_recognition as sr
import webbrowser
import win32com.client
import os
from playsound import playsound
import datetime
from config import gemini_api_key
import google.generativeai as genai

conversation = []

# user_history = []


def chat(prompt):
    global conversation
    # print(f"Role : User \nContent : {prompt}")
    
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
        system_instruction=f"you are david, a virtual assistant. you are provided with conversation history {conversation} and your work is to go through the history and analyze it. and if your input prompt is available in history then answer the input from conversation history and if the question is new to you then answer how you normally answer. answers should be to the point and short."
    )

    chat_session = model.start_chat(history = [])

    response = chat_session.send_message(prompt)
    response.resolve()
    
    conversation.append({"role" : "user" , "content" : prompt})
    conversation.append({"role" : "david","content" : response.text})
  
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

def conversation_appender(prompt, response = ""):
    conversation.append({"role" : "user" , "content" : prompt})
    conversation.append({"role" : "david","content" : response})

def classifier(command):
    prompt = f"classify the following statement in category of 'Command' or 'question' or 'normal' and return just that one word : {command}"
    result = gemini_ai(prompt)
    # print(result)
    return result.lower()

def new_classifier(command):
    prompt = f"go through {basic_category} and based on it classify the following statement in category of 'other' or 'normal' and return just that one word : {command}"
    result = gemini_ai(prompt)
    # print(result)
    return result.lower()

def cleaner(code_response):
    
    '''removes python word and other symbols from code response'''
    
    code_response1 = code_response.replace("python","")
    final_code_response = code_response1.replace("```","")
    return final_code_response
    
    

def summarizer(history):
    
    '''summarizes whole history'''
    
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
            # print(e)
            say("Some error occurred by David A I")


basic_category = {
    "other" : ["open text file", "open specific app/file" ,"create a new text file with name", "find specific folder", "give path of specific     file"] , 
    "normal" : ["remember something" , "recall it"]}

if __name__ == "__main__":
    say("Hello I am David A I")
    sites = [["Youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.org"],["google","https://google.com"]]
    while True:
        print("listening..")
        try: 
            command = takeCommand().lower()
            print(f"User : {command}")

            if "quit" in command :
                exit()
                
            if command=="david":
                continue
            
            category = classifier(command)
            
            if "command".lower() in category:
                print("Working on it Sir.")
                say("Working on it Sir.")
                
                new_category = new_classifier(command)
                # print(new_category)
                               
                if "open music" in command :
                    musicPath = "C:/Users/acer/Downloads/sample_music.mp3"
                    # playsound(musicPath) #alternate way
                    os.system(f"start {musicPath}")
                
                elif "clear conversation history".lower() in command:
                    conversation = []  
                    
                elif "conversation history".lower() in command :
                    # print("here")
                    print(conversation)
                                
                elif "other".lower() in new_category:
                    new_prompt = f"just return the code which will fulfill the command , just return the code of following command and nothing else : {command} consider that the device is of Windows OS"
                    code_response = gemini_ai(new_prompt)
                    final_code = cleaner(code_response)
                    conversation_appender(command,final_code)
                    # print(final_code)
                    exec(final_code)
                    
                else:
                    chat_response = chat(command)
                    conversation_appender(command,chat_response)
                    print(f"Role : David\nContent : {chat_response}")
                    say(chat_response)
                   
            elif "question".lower() in category:
                
                if "time" in command :
                    hour = datetime.datetime.now().strftime("%H")
                    mins = datetime.datetime.now().strftime("%M")
                    say(f"Current time is {hour} hours {mins} minutes")
                    
                else:
                    chat_response = chat(command)
                    conversation_appender(command,chat_response)
                    print(f"Role : David\nContent : {chat_response}")
                    say(chat_response)
                        
                  
            elif "artificial".lower() in command :
                prompt = command.split("intelligence",1)[1]
                response = gemini_ai(prompt)
                conversation_appender(command,chat_response)
                print(response)
              
            else:
                chat_response = chat(command)
                conversation_appender(command,chat_response)
                print(f"Role : David\nContent : {chat_response}")
                say(chat_response)
                
                
        except Exception as e:
            # print(e)
            pass
