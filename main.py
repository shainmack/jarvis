import os
import openai as ai
import speech_recognition
import pyaudio
import boto3
import pydub

ai.organization = 'org-YB5CGIuUYASqH4kd334vMaum'
ai.api_key = os.environ.get('OPENAI_API_KEY')

def query_ai(prompt):
    print('Prompt received: ', prompt)
    completions = ai.Completion.create(
        engine = 'text-davinci-003',
        prompt = prompt,
        max_tokens = 128,
        n = 1,
        stop = None,
        temperature = 0.5
    )
    message = completions.choices[0].text
    print('Message: ', message)
    return message


if __name__  == "__main__" :
    query_ai('how are you?')
