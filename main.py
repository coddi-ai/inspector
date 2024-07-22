import requests
import streamlit as st
import os
from openai import OpenAI
from io import BytesIO
import logging

def get_client():
    api_key = st.secrets["secret_key"]
    if not api_key:
        raise ValueError("No OpenAI API key found in environment variables")
    client = OpenAI(api_key=api_key)
    return client

def transcribe_audio(client, audio_file):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        language='es',
        file=audio_file,
    )
    return transcription.text

def refine_transcription(client, transcription, system_prompt='', temperature=0.8):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription}
        ]
    )
    return response.choices[0].message.content

def process_audio(audio_path):
    client = get_client()
    audio_file = open(audio_path, "rb")
    transcription = transcribe_audio(client, audio_file)
    # system_prompt = 
    # refined_transcription = refine_transcription(client, transcription, system_prompt)

    return transcription
