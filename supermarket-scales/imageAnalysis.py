
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
        prompt ="""Extract the following information: estimated weight, number, kind of vegetable or fruit."""
        prompt+="""Format the results in JSON text, ensuring to include the fields \"number\", \"kind\" . """
        prompt+="""The expected result characteristics are:"""
        prompt+="""The results must be accurate and reliable."""
        prompt+="""Kind is the kind of vegetable or fruits values should be one of this value : tomato, kiwi, cumcumber, apple, eggplant, clementine, unknown or Mixed. """
        prompt+="""number is the number of fruits or vegetable in the picture. """

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
        kind="Red"
        number=5

        return dict(extractedPictureElements=dict(kind=kind,number=number))