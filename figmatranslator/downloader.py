import requests
from typing import Dict, List
from .constants import Config
from .utils import downloadImage
from .models import FigmaImageResponse

class FigmaDownloader:
    def __init__(self):
        self.headers = {
            "X-Figma-Token": Config.FIGMA_API_KEY
        }

    def getFigmaFileImages(self, file_id: str) -> Dict:
        """
        Retrieve image URLs for all frames in a Figma file.
        """
        def extractFrameIDs(node):
            """
            Extracts relevant frame IDs from the Figma file.
            """
            frame_ids = []
            if node['type'] == 'FRAME':
                frame_ids.append(node['id'])
            if 'children' in node:
                for child in node['children']:
                    frame_ids.extend(extractFrameIDs(child))
                    break
            return frame_ids

        response = requests.get(f"https://api.figma.com/v1/files/{file_id}", headers=self.headers)
        file_data = response.json()

        frame_ids = extractFrameIDs(file_data['document'])

        image_params = {
            "ids": ",".join(frame_ids),
            "format": "png",
            "scale": "2"
        }
        response = requests.get(f"https://api.figma.com/v1/images/{file_id}", headers=self.headers, params=image_params)
        image_data = FigmaImageResponse(**response.json())
        
        return image_data.images
    
    def downloadFigmaFileImages(self, file_id: str, filename: str) -> List[str]:
        """
        Downloads all figma file images! Currently, this naively just downloads the first one. I need to update this to
        download more later on!
        """
        image_urls = self.getFigmaFileImages(file_id)
        if image_urls:
            first_key = next(iter(image_urls))
            first_url = image_urls[first_key]
            downloadImage(first_url, f"1_{filename}")
            return [f"1_{filename}"]
        else:
            print("No image URLs found to download.")

