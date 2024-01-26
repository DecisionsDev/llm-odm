
from langchain_community.llms import Ollama
import base64
from io import BytesIO
from PIL import Image

class ImageAnalysis:
    def __init__(self, model_name="llava"):
        self.bakllava = Ollama(model=model_name)

    @staticmethod
    def convert_to_base64(pil_image):
        """
        Convert PIL images to Base64 encoded strings.
        :param pil_image: PIL image
        :return: Base64 string
        """
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def analyze_image(self, file_path, question):
        """
        Analyzes an image and returns the LLM's response.
        :param file_path: Path to the image file
        :return: LLM's response
        """
        pil_image = Image.open(file_path)
        image_b64 = self.convert_to_base64(pil_image)
        llm_with_image_context = self.bakllava.bind(images=[image_b64])
        return llm_with_image_context.invoke(question)

