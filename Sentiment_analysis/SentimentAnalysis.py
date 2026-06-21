from flask import Flask,render_template
from flask import request as rq
import dotenv,os
from textblob import TextBlob

class EnvNotFoundError(Exception):
    def __init__(self, error=".env file for flask secret key not found.") -> None:
        super().__init__(error)

class SentimentAnalysis():
    def __init__(self) -> None:
        self.dir=os.path.dirname(__file__)
        self.envfilename=".env"
        self.path = str(os.path.join(self.dir,self.envfilename))
        try:
            if not os.path.exists(self.path):
                raise EnvNotFoundError
            
        except EnvNotFoundError:
            print("File missing:",self.path)
            with open(self.path,"w+") as file:
                file.write(r"FLASK_API_KEY=")
                print("An env file has been created. Make sure to set configurations.")

app = Flask(__name__)
sentimentAnalysis = SentimentAnalysis()
app.secret_key = dotenv.load_dotenv(sentimentAnalysis.path)

@app.route("/",methods=['GET','POST'])
def index():
    '''
    This function returns index page.
    '''
    try:
        return render_template("index.html",output=None),200
    except Exception as e:
        print(e)
        return "Could not load index.html",500

@app.route("/processText",methods=['POST'])
def processText():
    '''
    This function fetches the name=inputbox passed from index.html and does
    simple validation with textblob.
    '''
    try:
        text=None
        output=None
        error=None
        polarity=0
        subjectivity=0
        label="Neutral"
        if rq.method == "POST":
            text = rq.form.get("inputbox")
            output=True if text else None 

            if not text or text=='':
                error='Make sure you type a sentence and then try again.'
            
            blob = TextBlob(text)
            polarity = blob.polarity
            subjectivity = blob.subjectivity
            
            if polarity > 0.1:
                label = "Positive"
            elif polarity < -0.1:
                label = "Negative"
            else:
                label = "Neutral"

        return render_template("index.html",output=output,
                               error=error,
                               sentence=str(text),
                               sentiment=label,
                               polarity=polarity,
                               subjectivity=subjectivity),200
    except Exception as e:
        print(e)
        return "Could not load index.html",500
if __name__ == "__main__":
    app.run()
