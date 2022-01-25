from typing import final
import speech_recognition as sr
import spacy
from flask import logging, Flask, render_template, request, flash


app = Flask(__name__)
app.secret_key = "VatsalParsaniya"

@app.route('/')
def index():
    flash(" Welcome to Vatsal's site")
    return render_template('index.html')

@app.route('/audio_to_text/')
def audio_to_text():
    flash(" Press Start to start recording audio and press Stop to end recording audio")
    return render_template('audio_to_text.html')

@app.route('/audio', methods=['POST'])
def audio():
    r = sr.Recognizer()
    nlp = spacy.load("fr_core_news_sm")
    with open('upload/audio.wav', 'wb') as f:
        f.write(request.data)
  
    with sr.AudioFile('upload/audio.wav') as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='fr-FR', show_all=True)
        print(text)
        # return_text = " Vous avez dit: <br> "
        return_text=""
        try:
            return_text += text['alternative'][0]['transcript']
        except:
            return_text = " Erreur de detection"
        
    #Partie Benjamin 
    audio_text = nlp(return_text)

    # show entities
    finalText="Depart "
    departure=""
    destination=""
    for entity in audio_text.ents:
        #for i, token in enumerate(audio_text):            
            #if(entity.label_=="LOC" and  )
            #print(token.text, token.dep_)
        print(entity.text ,'|', entity.label_)
        if(len(finalText)>7):
            finalText+=" <br/>Destination : "
        finalText+=entity.text

        
    return str(finalText)


if __name__ == "__main__":
    app.run(debug=True)
