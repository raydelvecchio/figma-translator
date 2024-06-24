import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figmatranslator import FigmaTranslator

def testTranslation(figma_file_id: str):
    ft = FigmaTranslator(project_name="test", test_environment=True)
    ft.translate(figma_file_id=figma_file_id, output_image_filename="test.png")

if __name__ == "__main__":
    # testTranslation("taJmdTEys8iPUAhCZo9v2L")
    # testTranslation("Mdxys83dhEKxCB9RuYf10B")  # mobile
    testTranslation("cTCyORaM2ZT9TYBC4brOZX")
