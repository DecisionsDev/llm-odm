
from langchain_community.llms import Ollama
import base64
from io import BytesIO
from PIL import Image
import json, os, re
class ImageAnalysis:
    def __init__(self, server_url, model_name="llava:v1.6"):
        print("Using Ollma Server: "+str(server_url))
        self.bakllava = Ollama(base_url=server_url,model=model_name)

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

    def analyze_criteria_image(self, file_path, question):
        """
        Analyzes an image and returns the LLM's response.
        :param file_path: Path to the image file
        :return: LLM's response
        """

        # Extracting the file path from the tuple
        filename = file_path[0]

        # Using os.path.basename to extract the file name
#        image_name = os.path.basename(file_path)
#        print("DEBUG "+image_name)
        pil_image = Image.open(filename)
        image_b64 = self.convert_to_base64(pil_image)
        llm_with_image_context = self.bakllava.bind(images=[image_b64])
        return llm_with_image_context.invoke(question)

    def analyze_image(self, file_path):
        """
        Analyzes an image and returns the LLM's response.
        :param file_path: Path to the image file
        :return: LLM's response
        """
        prompt ="""Extract the following information: hair color, age, skin color and gender. """
        prompt+="""Format the results in JSON text, ensuring to include the fields \"hairColor\", \"age\", \"skinColor\" and \"gender\". """
        prompt+="""The expected result characteristics are: """
        prompt+="""The results must be accurate and reliable."""
        prompt+="""Gender values should Male or Female. """
        prompt+="""age should be a number. """
        prompt+="""skinColor should be one of this values Dark, Ebony, Ivory, Light, Medium or Unknown """
        prompt+="""hairColor should be one of this values  Black, Blonde, Brown, Gray, Red, White or Unknown. """

        resultllm = self.analyze_criteria_image(file_path,prompt)
  
        # Utilisation d'une expression régulière pour trouver tout ce qui est entre {}
        match = re.search(r'\{(.*?)\}', resultllm, re.DOTALL)
        result=resultllm

        if match:
            # Extraction et affichage du premier élément entre accolades
            result = "{"+match.group(1)+"}"
        else:
            print("Aucun contenu trouvé entre accolades.")
        print("Final Result from LLM : "+result)
#        age= self.analyze_criteria_image(file_path,"what is the age  ? Reply only the age")
#        skin = self.analyze_criteria_image(file_path,"what is the color of skin  ? Reply only Clear or Medium or Dark ")
#        gender = self.analyze_criteria_image(file_path,"Is it a woman or a man  ? Reply only by Woman or Man")
#        return dict(hair_color=hair_color,age=age,skin=skin,gender=gender)        
#        age=32
#        skin="Clear"
#        gender="Female"
        return dict(extractedPictureElements=json.loads(result))

    def fake_analyse(self, file_path):
        """
        Analyzes an image and returns the LLM's response.
        :param file_path: Path to the image file
        :return: LLM's response
        """
#        hair_color = self.analyze_criteria_image(file_path,"what is the hair color ? Reply only the color")

#        age= self.analyze_criteria_image(file_path,"what is the age  ? Reply only the age")

#        skin = self.analyze_criteria_image(file_path,"what is the color of skin  ? Reply only Clear or Medium or Dark ")

#        gender = self.analyze_criteria_image(file_path,"Is it a woman or a man  ? Reply only by Woman or Man")
        hair_color="Red"
        age=5
        skin="Light"
        gender="Female"
        return dict(extractedPictureElements=dict(hairColor=hair_color,age=age,skinColor=skin,gender=gender))