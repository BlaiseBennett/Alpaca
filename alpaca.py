#Alpaca debug
#Contains all print statements for debugging.
#May slightly slow things down so just be aware

#Speech Recognition
import speech_recognition
#Ai Library
import ollama
#TTS libraries
from gtts import gTTS
from playsound import playsound

#speech recognition wakeword
wakeword = "alpaca"

def voiceDetection(wakeword):
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print("speak")
            audio = recognizer.listen(source)

            try:

                transcription = recognizer.recognize_google(audio).lower()
                print(f"said {transcription}")

                if wakeword in transcription:
                    print("wakeword detected")
                    print("speak again")
                    audio = recognizer.listen(source)

                    try:
                        question = recognizer.recognize_google(audio).lower()
                        print(question)
                        return question
                        break


                    except speech_recognition.RequestError:
                        print("google masterminds have failed you.")

                    except speech_recognition.UnknownValueError:
                        break
            

            except speech_recognition.RequestError:
                print("No connection to the Google Mastermind Servers")

            except speech_recognition.UnknownValueError:
                continue

def prompt():
    #Use all the good voice detection stuff
    question = voiceDetection(wakeword)
    #Ai Model
    response = ollama.chat(model='tinyllama', messages=[
        {
            'role': 'user',
            'content': question,
        },
    ])

    #Audio Output
    tts = gTTS(response['message']['content'])
    tts.save('response.mp3')
    playsound('response.mp3')

#make an infinite loop because thats how we do it here and also any other way (just running it inside) breaks it
x = 0
while x == 0:    
    prompt()
