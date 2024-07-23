import streamlit as st
import requests
import os
from openai import OpenAI
from io import BytesIO
import logging

def get_client():
    try:
        api_key = os.getenv("OPENAI_API_KEY")
    except:
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

def refine_transcription(client, transcription, temperature=0.8):
    system_prompt = """
Eres un asistente que extrae la información relevante para explicar una inspección visual. 
Transforma el texto entregado, para que explique de manera clara y concisa lo observado en la inspección, centrandose en los hechos y observaciones generadas.
El contexto de los reportes es en contexto minero, haciendo inspecciones manuales sobre equipos, por lo cual se espera que se utilicen conceptos técnicos de minería y mecanica.
El texto generado debe tener el siguiente formato:
Fecha (si es que está disponible)
* Observaciones (en bullet points).

Errores comunes:
palaciete = Pala 7
"""
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
    transcription = refine_transcription(client, transcription)

    return transcription