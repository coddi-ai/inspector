import streamlit as st
from utils import *
from PIL import Image
import time
import subprocess
from dotenv import load_dotenv
import os
from audio_recorder_streamlit import audio_recorder

load_dotenv()

# Sidebar for machine and component information
st.sidebar.header("Machine and Component Information")
machine = st.sidebar.text_input("Machine")
component = st.sidebar.text_input("Component")

# Set up the Streamlit app
st.title("Image and Audio Upload MVP")


# Capture image using camera
st.header("Capture an Image")
uploaded_image = st.camera_input("Take a picture")
image_buffer = None
audio_buffer = None

# Image upload
if uploaded_image is not None:
    image_buffer = bytes(uploaded_image.getbuffer())
    # Display the captured image
    image = Image.open(uploaded_image)
    st.image(image, caption="Captured Image", use_column_width=True)

# Audio upload
st.header("Upload an Audio File")
uploaded_audio = audio_recorder(text = 'Record audio',
                                # energy_threshold = (-1,1),
                                pause_threshold = 2.0,)
if uploaded_audio is not None:
    audio_buffer = uploaded_audio
    # Display the uploaded audio file
    st.audio(uploaded_audio, format='audio/mpeg')

# Process button
if uploaded_image is not None and uploaded_audio is not None:
    if st.button("Process"):
        print("Uploading files to Azure Storage...")
        upload_time = int(time.time())
        image_blob_name = f"upload_{upload_time}/image.jpg"
        audio_blob_name = f"upload_{upload_time}/audio.mp3"

        print("Uploading images to Azure Storage...")
        # Upload both files to Azure Storage
        image_url, audio_url = upload_files_to_azure(image_buffer, audio_buffer, image_blob_name, audio_blob_name)

        print(f"Urls of the uploaded files: \n{image_url} \n{audio_url}")

        processed_audio_result = process_audio(audio_blob_name)
        if processed_audio_result[1] == 0:
            st.write(f"Error: {processed_audio_result[0]}")
        else:
            st.write(f"{processed_audio_result[0]}")
else:
    st.write("Please fill in all the information and upload both files to proceed.")
