import os
import openai as ai
import speech_recognition as sr
from boto3 import Session
# from botocore.exceptions import BotoCoreError, ClientError
from pydub import AudioSegment
from pydub.playback import play

# import pyaudio
# import sys
# import subprocess
# from tempfile import gettempdir
# from contextlib import closing

ai.organization = 'org-YB5CGIuUYASqH4kd334vMaum'
ai.api_key = os.environ.get('OPENAI_API_KEY')
wake_word = 'hey jarvis'


def query_ai(prompt):
    print('Prompt received: ', prompt)
    completions = ai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].text
    print('Message: ', message)
    return message


def listen_for_wake_word():
    r = sr.Recognizer()

    with sr.Microphone(0) as source:
        print('Listening for wake word')
        audio = r.listen(source, 10, 3)
        try:
            speech = r.recognize_google(audio)
            print(speech)
            if "hey jarvis" in speech.lower():
                print('\033[92mwake word detected\033[0m')
                audio_cmd = r.listen(source, 5, 15)
                cmd = r.recognize_google(audio_cmd)
                print('Command: ', cmd)
                response = query_ai(cmd)
                speak(response)
            else:
                print('\033[93wake word NOT detected\033[0m')
        except sr.RequestError:
            print('Request error')
        except sr.UnknownValueError:
            print('Unknown Value Error: I didn\'t catch that...')
        except sr.WaitTimeoutError:
            print('WaitTimeoutError: You took too long to speak.')
    return


def speak(content):
    session = Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1'
    )
    polly = session.client('polly')
    speech = polly.synthesize_speech(
        Text=content,
        OutputFormat='mp3',
        VoiceId='Brian'
    )
    audio = speech['AudioStream'].read()
    print('creating mp3 file')
    filename = 'jarvis.mp3'
    with open(filename, 'wb') as file:
        file.write(audio)
        file.close()
    clip = AudioSegment.from_mp3(filename)
    play(clip)


if __name__ == "__main__":
    # query_ai('how are you?')
    while True:
        listen_for_wake_word()
    # speak(query_ai('what\'s the best programming language?'))
    # print('It works')
