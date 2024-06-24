import requests
import os
from .constants import Config
import os
import subprocess

def downloadImage(image_url: str, output_filename: str):
    """
    Download images from URLs and save them to the specified directory.
    """
    os.makedirs(Config.IMAGES_FOLDER, exist_ok=True)
    
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(os.path.join(Config.IMAGES_FOLDER, output_filename), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded Image: {output_filename}")
    else:
        print(f"Failed to download image {output_filename}")
        
def runCommand(command):
    """
    Runs a command as if from the terminal.
    """
    print(f"Running command: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(stderr.decode())
        exit(1)
    return stdout.decode()

def createFile(path, content):
    """
    Runs a command as if from the terminal.
    """
    print(f"Creating file: {path}")
    with open(path, 'w') as f:
        f.write(content)
