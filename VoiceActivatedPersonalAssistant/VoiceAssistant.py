import os,dotenv,re,locale
from word2number import w2n
from multiprocessing import Process,Value
import keyboard
import pyttsx3 
import requests
import speech_recognition as sr
from datetime import datetime,timedelta

class EnvNotFoundError(Exception):
    def __init__(self,error=".env file for keys not found.") -> None:
        super().__init__(error)
class MicrophoneNotFoundError(Exception):
    def __init__(self,error="Microphone not found") -> None:
        super().__init__(error)

class VoiceAssistant:
    def __init__(self) -> None:
        self.ongoingReminder=Value('b',False)
        self.localInfo = locale.getlocale()[0]
        self.APIS={"WEATHER_API_URL":"",
                   "WEATHER_API":"",
                   "NEWS_API_URL":"",
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
                    self.APIS[key]=os.getenv(key)
                
            if not sr.Microphone.list_microphone_names():
                raise MicrophoneNotFoundError
            else:
                for index,mic in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Devices available: {mic} for Microphone(device_index={index})")
                    self.mic_dict[index] = mic
            
        except EnvNotFoundError:
            with open(self.path,"w+") as file:
                file.write("WEATHER_API_URL=https://api.weatherapi.com/v1\n")
                file.write("WEATHER_API=\n")
                file.write("NEWS_API_URL=https://newsapi.org/v2/everything\n")
                file.write("NEWS_API=")
                print("An env file has been created. Make sure to set configurations.")
        except MicrophoneNotFoundError:
            pass
                
    def processToNumber(self,captured_speech:str):
        try:
            if not captured_speech:
                print("No speech captured for number parsing.")
                return 0
            
            processed_num = 0
            cleaned = " ".join(self.processText(captured_speech))
            print("Data inputted:",cleaned)
            processed_num = float(w2n.word_to_num(cleaned))
            return processed_num
        except ValueError as e:
            processed_num = re.findall(r"\d+",captured_speech)
            if len(processed_num) > 0:
                processed_num = float(processed_num[0])
            else:
                processed_num=0
            print("Processed:",processed_num)
            return processed_num
        except Exception as e:
            print(e)
            return 0
        
    @staticmethod    
    def setReminder(task,delay=60,ongoing={}):
        import pyttsx3,time
        ongoing.value = True

        def speakMessage(msg):
            engine.say(msg)
            engine.startLoop(False)
            while engine.isBusy():
                engine.iterate()
            engine.endLoop()
            return

        print("Task name:",task)
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        minute = delay/60
        print("delay in minutes:",minute)
        speakMessage(f"Reminder set for {task}! I will remind you in {minute} minutes.")
        
        time.sleep(delay)
        speakMessage(f"Your timer for {minute} minutes ended!")
        print("Task completed.")
        ongoing.value = False
        engine.stop()
        return
         
    def readNews(self,parameter="India",startDate=datetime.strftime(datetime.now()- timedelta(days=1),'%Y-%m-%d')):
        '''
        This function will read at least 1 article. Max 3.
        '''
        try:
            call_url = f"{self.APIS['NEWS_API_URL']}?q={parameter}&from={startDate}&sortBy=publishedAt&apiKey={self.APIS['NEWS_API']}"
            response = requests.get(call_url)
            data = response.json()

            news_to_read=3
            self.speakMessage(f"I will read {news_to_read} headlines.")
            
            for index in range(news_to_read):
                self.speakMessage(f"Speaking headline {index+1}")
                article = data['articles'][index]
                source = article['source']['name']
                author = article['author']
                title = article['title']
                description = article['description']
                publishedAt = article['publishedAt']
                self.speakMessage(f"{source}, Title: {title}, Author: {author}.")
                self.speakMessage(f"Description: {description}. Published at: {publishedAt}")
        except Exception:
            call_url = f"{self.APIS['NEWS_API_URL']}?q={parameter}&from={startDate}&sortBy=publishedAt&apiKey={self.APIS['NEWS_API']}"
            response = requests.get(call_url)
            data = response.json()

            news_to_read=1
            self.speakMessage(f"I will read {news_to_read} headline/s")
            
            for index in range(news_to_read):
                self.speakMessage(f"Speaking headline {index+1}")
                article = data['articles'][index]
                source = article['source']['name']
                author = article['author']
                title = article['title']
                description = article['description']
                publishedAt = article['publishedAt']
                self.speakMessage(f"{source}, Title: {title}, Author: {author}.")
                self.speakMessage(f"Description: {description}. Published at: {publishedAt}")
            raise

    def readWeather(self,country="India"):
        try:
            call_url=rf"{self.APIS['WEATHER_API_URL']}/forecast.json?key={self.APIS['WEATHER_API']}&q={country}&days=1&aqi=yes&alerts=yes"
            response= requests.get(call_url)
            data = response.json()
            curr_city = data['location']['name']
            country = data['location']['country']
            
            temperature= data['current']['temp_c']
            atmosphere= data['current']['condition']['text']
            feels_like= data['current']['feelslike_c']
            humidity= data['current']['humidity']
            wind_kph= data['current']['wind_kph']
            
            day = data['forecast']['forecastday'][0]['day']
            max_temp= day['maxtemp_c']
            min_temp= day['mintemp_c']
            rain_chance= day['daily_chance_of_rain']

            alerts= data['alerts']['alert']
            print("Alerts for weather:",alerts)

            self.speakMessage(
        f"""Weather in {curr_city}, {country}. {atmosphere}, {temperature} degrees. 
        This feels like {feels_like} where humidity is {humidity} percent. Chances of rain is {rain_chance} percent.
        Your area's temperature ranges from: {min_temp} to {max_temp}, winds reaching {wind_kph} per hour.
        """)
        except Exception:
            call_url=rf"{self.APIS['WEATHER_API_URL']}/forecast.json?key={self.APIS['WEATHER_API']}&q=India&days=1&aqi=yes&alerts=yes"
            response= requests.get(call_url)
            data = response.json()
            curr_city = data['location']['name']
            country = data['location']['country']
            
            temperature= data['current']['temp_c']
            atmosphere= data['current']['condition']['text']
            feels_like= data['current']['feelslike_c']
            humidity= data['current']['humidity']
            wind_kph= data['current']['wind_kph']
            
            day = data['forecast']['forecastday'][0]['day']
            max_temp= day['maxtemp_c']
            min_temp= day['mintemp_c']
            rain_chance= day['daily_chance_of_rain']

            alerts= data['alerts']['alert']
            print("Alerts for weather:",alerts)

            self.speakMessage(
            f"""Weather in {curr_city}, {country}. {atmosphere}, {temperature} degrees. 
            This feels like {feels_like} where humidity is {humidity} percent. Chances of rain is {rain_chance} percent.
            Your area's temperature ranges from: {min_temp} to {max_temp}, winds reaching {wind_kph} per hour.
            """)
            raise
            

    def speakMessage(self, msg):
        try:
            self.engine.say(msg)
            self.engine.startLoop(False)
            while self.engine.isBusy():
                self.engine.iterate()
            self.engine.endLoop()
        except Exception as e:
            print(e)
    def listenMessage(self):
        try:
            self.recognizer = sr.Recognizer()
            with sr.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic,duration=1)
                audio = self.recognizer.listen(mic,timeout=2)
                text = self.recognizer.recognize_whisper(audio,model="small",language="english")
                return text
        except sr.UnknownValueError:
            raise 
        except sr.WaitTimeoutError:
            return None
        
    def processText(self,text:str):
        cleaned=""
        for letter in text:
            if letter.isalnum() or letter.isspace():
                cleaned += letter.lower()
        return cleaned.split()
    
    def decideOperation(self,text):
        cleaned_message = self.processText(text)
        current_country = self.localInfo.split('_')
        current_country = current_country[-1]
        if 'weather' in cleaned_message:          
            self.speakMessage("Please wait, let me fetch weather data.")
            self.readWeather(country=current_country)
        elif 'news' in cleaned_message:       
            self.speakMessage("Please wait, let me fetch news data.")
            self.readNews(parameter=current_country)
        elif 'reminder' in cleaned_message:

            if self.ongoingReminder.value:
                print("An on going reminder is set. Make sure to let this reminder finish.")
                print("----")
                return
            
            seconds=0
            count=0
            self.speakMessage("Ok, Speak task name.")
            print("Say your task name...")
            taskname = self.listenMessage()

            self.speakMessage("Now speak number of minutes to remind you. Example: 1 minute")
            print("Now speak number of minutes to remind you. Example: 1 minute")
            captured_speech = self.listenMessage()
            
            count = assistant.processToNumber(captured_speech)
            
            if count and count >= 1 :
                seconds = int(count * 60)
            else:
                seconds = 60
                self.speakMessage("Could not understand minute count. timer will be set to 1 minute.")

            reminder_process = Process(target=self.setReminder,kwargs={"task":taskname,"delay":seconds,"ongoing":self.ongoingReminder})
            reminder_process.start()

        elif 'exit' in cleaned_message or 'quit' in cleaned_message:
            self.speakMessage("Exitting... Thankyou for using!")
            exit(0)
        else:
            self.speakMessage("Could not understand. Please speak clearly.")
            
if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.speakMessage("Welcome to Voice Assistant. What would you like to do?")
    assistant.speakMessage("A) Set a reminder. B) Check current weather. C) Check current news.")
    rate = assistant.engine.getProperty('rate')
    assistant.engine.setProperty('rate',150)
    print("Listening...")
    
    while True:
        try:
            if keyboard.is_pressed('m'):
                print("-------")
                print("To change microphone, input device_index")
                device_index = int(input("device_index="))
                if assistant.mic_dict[device_index]:
                    print(f"Switching to {assistant.mic_dict[device_index]}")
                    print("-------")
                    sr.Microphone(device_index=device_index)
                print("Listening...")
            else:
                captured_speech = assistant.listenMessage()
                if not captured_speech or captured_speech == '':
                    continue
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
