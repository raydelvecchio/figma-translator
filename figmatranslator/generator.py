import anthropic
import base64
import time
import os
from .constants import Config

class UIGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

    def getCodeForImage(self, image_filename: str) -> str:
        start_time = time.time()

        prompt = """
        The assistant is a frontend engineer. The assistant's job is to create frontend code based on the designer's designs in a larger workflow.

        The assistant will receive a design, and must implement it. The implementation should include all styling, components, and imports as
        necessary. The assistant will also include comments on the lines where another engineer must implement some downstream action detailing what's left to build.

        The assistant's environment has the following installed:
        - React.js
        - Tailwind CSS
        - Javascript
        - Bootstrap, initialized in index.js
        - react-icons

        The assistant must only use these components to create the application.

        Format the output code as a single file, with one `export default` at the bottom to use the component. Break down each part
        into smaller components for enhanced readability. Don't be afraid of interactivity! Make the components reactive.

        In the assistant's response, provide a brief explanation of the code in the comments before any implementation.

        Output nothing else in addition to your explanation, comments, and implementation. No text can be processed.
        """

        with open(f"{Config.IMAGES_FOLDER}/{image_filename}", "rb") as f:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": base64.b64encode(f.read()).decode(),
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt,
                            },
                        ],
                    }
                ],
            )
        
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Time to code for {image_filename}: {execution_time:.2f} seconds")

        code_response = message.content[0].text

        os.makedirs(Config.CODE_FOLDER, exist_ok=True)
        output_file = f"{Config.CODE_FOLDER}/{image_filename.split('.')[0]}.js"
        with open(output_file, "w") as f:
            f.write(code_response)
        
        return output_file
