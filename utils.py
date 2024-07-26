import streamlit as st
import requests
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

def get_function_url():
    try:
        if ".env" in os.listdir():
            load_dotenv()
            function_url = os.getenv("FUNCTION_URL_AZURE")
            subscription_key = os.getenv("SUBSCRIPTION_KEY")
        else:
            function_url = st.secrets["FUNCTION_URL_AZURE"]
            subscription_key = st.secrets["SUBSCRIPTION_KEY"]

        if not function_url or not subscription_key:
            raise ValueError("Function URL or Subscription Key not found in environment variables")

        return function_url, subscription_key

    except Exception as e:
        raise ValueError(f"No function URL or Subscription Key found in environment variables: {e}")

def get_azure_credentials():
    try:
        if ".env" in os.listdir():
            load_dotenv()
            connect_str = os.getenv("AZURE_CONNECTION_STRING")
            container_name = os.getenv("AZURE_CONTAINER_NAME")
        else:
            connect_str = st.secrets["AZURE_CONNECTION_STRING"]
            container_name = st.secrets["AZURE_CONTAINER_NAME"]

        if not connect_str or not container_name:
            raise ValueError("Azure Storage connection string or container name not found in environment variables")

        return connect_str, container_name

    except Exception as e:
        raise ValueError(f"No Azure Storage connection string or container name found in environment variables: {e}")

def upload_to_azure(file_buffer, file_name, connect_str, container_name):
    """
    Uploads a file to Azure Blob Storage.
    
    Args:
    - file_buffer: The file buffer to upload.
    - file_name: The name of the file in Azure Blob Storage.
    - container_name: The name of the Azure container.
    - connect_str: The connection string for Azure Blob Storage.
    
    Returns:
    - file_url: The URL of the uploaded file.
    """
    # Initialize Azure Storage Blob client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    # Get the blob client
    blob_client = container_client.get_blob_client(file_name)
    # Upload the file
    blob_client.upload_blob(file_buffer, overwrite=True)
    
    # Get the URL of the uploaded file
    file_url = blob_client.url
    return file_url

def upload_files_to_azure(image_buffer, audio_buffer, image_name, audio_name):
    """
    Uploads both image and audio files to Azure Blob Storage.
    
    Args:
    - image_buffer: The image file buffer to upload.
    - audio_buffer: The audio file buffer to upload.
    - image_name: The name of the image file in Azure Blob Storage.
    - audio_name: The name of the audio file in Azure Blob Storage.
    - container_name: The name of the Azure container.
    - connect_str: The connection string for Azure Blob Storage.
    
    Returns:
    - image_url: The URL of the uploaded image file.
    - audio_url: The URL of the uploaded audio file.
    """
    container_name, connect_str = get_azure_credentials()
    image_url = upload_to_azure(image_buffer, image_name, container_name, connect_str)
    audio_url = upload_to_azure(audio_buffer, audio_name, container_name, connect_str)
    return image_url, audio_url

def process_audio(audio_file_name):
    function_url, subscription_key = get_function_url()
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    payload = {"file_name": audio_file_name}

    print("Sending request to the function...")
    print(function_url,'\n',subscription_key,'\n',payload,'\n',headers)

    response = requests.post(function_url, json=payload, headers=headers)

    if response.status_code == 200:
        return (response.text, 1)
    else:
        return (f"Error: {response.status_code} - {response.text}", 0)
