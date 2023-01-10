import os
import openai as ai
import speech_recognition
import pyaudio
import boto3
import pydub

ai.organization = 'org-YB5CGIuUYASqH4kd334vMaum'
ai.api_key = os.environ.get('OPENAI_API_KEY')

if __name__  == "__main__" :
    print("It works!")
