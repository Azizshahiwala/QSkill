import os,dotenv
import keyboard
import pyttsx3 
import requests
import speech_recognition as sr

class EnvNotFoundError(Exception):
    def __init__(self,error=".env file for keys not found.") -> None:
        super().__init__(error)
class MicrophoneNotFoundError(Exception):
    def __init__(self,error="Microphone not found") -> None:
        super().__init__(error)

class VoiceAssistant:
    def __init__(self) -> None:
        self.APIS={"WEATHER_API_URL":"",
                   "WEATHER_API":"",
                   "NEWS_API":""}
        self.mic_dict = {}
        self.recognizer = None
        self.engine = pyttsx3.init()
        self.dir=os.path.dirname(__file__)
        self.envfilename=".env"
        self.path = str(os.path.join(self.dir,self.envfilename))
        try:
            if not os.path.exists(self.path):
                raise EnvNotFoundError 
            else:
                dotenv.load_dotenv(self.path)
                keys = self.APIS.keys()
                for key in keys:
                    print("key:",key)
                    self.APIS[key]=os.getenv(key)
                print("Dictionary:",self.APIS)

            if not sr.Microphone.list_microphone_names():
                raise MicrophoneNotFoundError
            else:
                for index,mic in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Microphone available: {mic} for Microphone(device_index={index})")
                    self.mic_dict[index] = mic
            
        except EnvNotFoundError:
            with open(self.path,"w+") as file:
                file.write("WEATHER_API_URL=https://api.weatherapi.com/v1\n")
                file.write("WEATHER_API=\n")
                file.write("NEWS_API=")
                print("An env file has been created. Make sure to set configurations.")
        except MicrophoneNotFoundError:
            pass
    def showNews(self):
        pass 
    def showWeather(self,city="Ahmedabad"):
        '''
        This function fetches api response from url and gets fields.
        '''
        call_url=rf"{self.APIS['WEATHER_API_URL']}/forecast.json?key={self.APIS['WEATHER_API']}&q={city}&days=1&aqi=yes&alerts=yes"
        response= requests.get(call_url)
        data = response.json()
        curr_city = data['location']['name']
        country = data['location']['country']
        
        temperature= data['current']['temp_c']
        atmosphere= data['current']['condition']['text']
        feels_like= data['current']['feelslike_c']
        humidity= data['current']['humidity']
        wind_kph= data['current']['wind_kph']
        uv_index= data['current']['uv']
        
        day = data['forecast']['forecastday'][0]['day']
        max_temp= day['maxtemp_c']
        min_temp= day['mintemp_c']
        rain_chance= day['daily_chance_of_rain']

        alerts= data['alerts']['alert']
        print("alerts:",alerts)
        self.speakMessage(
    f"Weather in {curr_city}, {country}. "
    f"{atmosphere}, {temperature} degrees. "
    f"Feels like {feels_like}. "
    f"Humidity {humidity} percent. "
    f"Chance of rain: {rain_chance} percent."
    f"Temperature ranges from: {min_temp} to {max_temp}."
    f"Wind kilometer per hour: {wind_kph}"
    f"UV index: {uv_index}")

    def speakMessage(self, msg):
        try:
            self.engine.say(msg)
            self.engine.startLoop()
            self.engine.endLoop()
        except Exception as e:
            print(e)
    def listenMessage(self):
        try:
            self.recognizer = sr.Recognizer()
            with sr.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic,duration=0.2)
                audio = self.recognizer.listen(mic)
                text = self.recognizer.recognize_whisper(audio,model="base",language="english")
                return text
        except sr.UnknownValueError:
            raise 
    def processText(self,text:str):
        cleaned=""
        for letter in text:
            print(letter)
            if letter.isalnum() or letter.isspace():
                cleaned += letter.lower()
        return cleaned.split()
    
    def decideOperation(self,text):
        cleaned_message = self.processText(text)

        if 'weather' in cleaned_message:
            print("User wants to see weather")
            self.showWeather()
        elif 'news' in cleaned_message:
            print("User wants to see news")
            self.showNews()
        elif 'reminder' in cleaned_message:
            print("User wants to set reminder")
        elif 'exit' in cleaned_message:
            self.speakMessage("Exitting... Thankyou for using!")
            exit(0)
        else:
            self.speakMessage("Could not understand. Please speak clearly.")
            
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.speakMessage("Welcome to Voice Assistant. What would you like to do?")
    assistant.speakMessage("A) Set a reminder. B) Check current weather. C) Check current news. D) Change microphone by pressing M.")

    while True:
        try:
            captured_speech = assistant.listenMessage()
            assistant.decideOperation(captured_speech)
        except IOError as e:
            print(e)
            continue
        except sr.UnknownValueError:
            assistant.recognizer = sr.Recognizer()
            continue
        except Exception as e:
            print(e)
            continue

'''

if keyboard.is_pressed('m'):
                print("-------")
                print("To change microphone, input device_index")
                device_index = int(input("device_index="))
                if assistant.mic_dict[device_index]:
                    print(f"Switching to {assistant.mic_dict[device_index]}")
                    print("-------")
                    sr.Microphone(device_index=device_index)
                continue

                

        
'''