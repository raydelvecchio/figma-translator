import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    FIGMA_API_KEY = os.getenv("FIGMA_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    IMAGES_FOLDER = "figma_images"
    CODE_FOLDER = "figma_code"
    ENVIRONMENTS_FOLDER = "environments"
    