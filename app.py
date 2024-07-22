import streamlit as st
from aux_func import process_audio
from PIL import Image
import os
import time

# Function to store data (dummy function)
def store_data(image_path, audio_path, machine, component):
    st.write(f"Image stored at: {image_path}")
    st.write(f"Audio stored at: {audio_path}")
    st.write(f"Machine: {machine}")
    st.write(f"Component: {component}")

# Set up the Streamlit app
st.title("Image and Audio Upload MVP")

# Create a base directory to save the uploaded files
base_upload_dir = "uploads"
if not os.path.exists(base_upload_dir):
    os.makedirs(base_upload_dir)

# Sidebar for machine and component information
st.sidebar.header("Machine and Component Information")
machine = st.sidebar.text_input("Machine")
component = st.sidebar.text_input("Component")

# Capture image using camera
st.header("Capture an Image")
uploaded_image = st.camera_input("Take a picture")
image_path = None
audio_path = None

if uploaded_image is not None:
    # Generate a unique directory name based on the current time
    upload_time = int(time.time())
    upload_dir = os.path.join(base_upload_dir, f"upload_{upload_time}")
    os.makedirs(upload_dir, exist_ok=True)

    # Save the captured image
    image_path = os.path.join(upload_dir, "image.jpg")
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    # Display the captured image
    image = Image.open(uploaded_image)
    st.image(image, caption="Captured Image", use_column_width=True)

# Audio upload
st.header("Upload an Audio File")
uploaded_audio = st.file_uploader("Record an audio...", type=["mp3", "wav", "ogg"])
if uploaded_audio is not None:
    if image_path is not None:
        # Save the uploaded audio in the same directory as the image
        audio_path = os.path.join(upload_dir, uploaded_audio.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())
        # Display the uploaded audio file
        st.audio(uploaded_audio, format='audio/' + uploaded_audio.name.split('.')[-1])

# Process button
if uploaded_image is not None and uploaded_audio is not None and machine and component:
    if st.button("Process"):
        st.write("Processing audio...")
        processed_audio_result = process_audio(audio_path)
        # store_data(image_path, audio_path, machine, component)
        # st.write("Processing complete. Files have been stored.")
        st.write(f"{processed_audio_result}")
else:
    st.write("Please fill in all the information and upload both files to proceed.")
