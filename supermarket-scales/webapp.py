import gradio as gr
import os
import time
from langchain_community.llms import Ollama
from imageAnalysis import ImageAnalysis
from invokeRuleServer import InvokeRuleServer
import base64
from io import BytesIO
import os,json
#from IPython.display import HTML, display
from PIL import Image
# Chatbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.
# Chemin vers ton dossier d'images
image_folder = 'data/samples'


def check_env():
    odm_server_url=os.getenv("ODM_SERVER_URL")
    if odm_server_url is None:
        print("You should set the Envirnment variable ODM_SERVER_URL. ODM_SERVER_URL=http://odm:9060")
    ollama_server_url=os.getenv("OLLAMA_SERVER_URL","http://localhost:11434")
    if ollama_server_url is None:
        print("You should set the Envirnment variable ODM_LLAMA_URL. OLLAMA_SERVER_URL=http://localhost:11434. Using default URL : http://localhost:11434 ")
    return odm_server_url,ollama_server_url

odm_server_url,ollama_server_url=check_env()
image_analysis = ImageAnalysis(server_url=ollama_server_url)

rule_server = InvokeRuleServer(odm_server_url)

def extractRulesTraceInformations(props):
    link=''
    name=''
    for prop in  props:
        if prop['name'] == 'ilog.rules.teamserver.elementID':
            # Extraire et afficher la valeur de 'value' pour cette propriété
            link="http://odmAdmin:odmAdmin@localhost:9060/decisioncenter/t/library#editor?baselineId=brm.Branch:1:1&id="+prop['value']
        if prop['name'] == 'ruleExecutionShortName':
            # Extraire et afficher la valeur de 'value' pour cette propriété
            name=prop['value']

    return name,link

def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)

def on_select_gallery_image(evt: gr.SelectData):  # SelectData is a subclass of EventData
    global selected_image
    selected_image=evt.value['image']['path']
    print("on_select_gallery_image"+selected_image)

def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

def add_file(history, file):
    if(file is not None): filename=file 
    elif selected_image is not None: 
        filename=selected_image
    else:
        print("Error no file selected")
    history = history + [((filename,), None)]
    return history

def displayBotMessage(history, message, raz):
    if raz == True: history[-1][1] = ""
    for character in message:
        history[-1][1] += character
        #time.sleep(0.01)
        yield history

def formatImageAnalysis(rulesParameters):
    print("Format Image"+str(rulesParameters))
    params=rulesParameters['extractedPictureElements']
    markdownResponse="""\n- Number : """+str(params['number'])+"\n"
    markdownResponse+="""- Kind : """+params['kind']+"\n"
    return markdownResponse

def format_to_markdown(data):
    markdown_text = ""
    friendlyName={
                  "tailoredProductNames":"Shop",
                  "tailoredMessaging":"Recommandations ",
                  "tailoredProducts":"Product suggestion",
                  "tailoredChannels":"Channel",
                  "discount":"Discount"
                  }
    for key, items in data['adProposal'].items():
        title=  friendlyName.get(key, key)  # Utilise la clé elle-même comme titre par défaut
        if hasattr(items, "__len__") and len(items) != 0:
            # Ajout de chaque élément de la liste comme point de puce
            markdown_text += f"### {title}\n"
            for item in items:
                if(key == "tailoredProductNames"):
                    item="<img src=\"file/data/shop/"+item+"\"/>"
                    markdown_text += f"{item}\n"
                else: 
                    markdown_text += f"- {item}\n"
            # Ajout d'un saut de ligne entre les sections pour une meilleure lisibilité
            markdown_text += "\n"
        else:
            if(key == "discount") and items > 0.0:                 
                title=  friendlyName.get(key, key)  # Utilise la clé elle-même comme titre par défaut
                markdown_text += f"### **{title} : <span style=\"color:blue\">{items} %</span>**"
    markdown_text +=f"\n**Decision Taken :**"
    for item in data['__decisionTrace__']['rulesFired']['ruleInformation']:
        name, link = extractRulesTraceInformations(item['properties']['property'])
        markdown_text +=f" ["+name+"]("+link+")&nbsp;,  "
        

    return markdown_text

def formatDecisionResponse(message):
    if "error" in message:
        return message['error']
    return format_to_markdown(message)



def bot(history):
    image=history[-1][0]
    rulesParameters=image_analysis.analyze_image(image)
    for updated_history in displayBotMessage(history, "**Analyse pitcture with LLM**</br>",True): yield updated_history
#    rulesParameters=image_analysis.fake_analyse(image)

    for updated_history in displayBotMessage(history, formatImageAnalysis(rulesParameters),False): yield updated_history
 #   for updated_history in displayBotMessage(history, "\n\n**Compute Recommandation with Decision Engine**\n",False): yield updated_history
 #   decisionResponse = rule_server.invokeRules(rulesParameters)
 #   for updated_history in displayBotMessage(history, formatDecisionResponse(decisionResponse),False): yield updated_history

# Récupère les chemins des images pour la galerie
image_paths = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg'))]
check_env()
with gr.Blocks() as demo:
    with gr.Row():
        gr.HTML("<h1>Product recommandation - Operation Decision Manager with Vision Assistant</h1>")

    chatbot =  gr.Chatbot(
            [],
            label="chatbot",
            elem_id="chatbot",
            bubble_full_width=False,
            avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
        )

    with gr.Row():
        gallery = gr.Gallery(label="Sample Galery", value=image_paths , columns=[3], rows=[1], object_fit="cover", height=300)
        btn_img = gr.Image(type="filepath", height=300)
    with gr.Row():
        btn = gr.Button("Analyse image")
    with gr.Row():
        gr.HTML("Select or upload a photo and click on Analyse image. Use <b>odmAdmin/odmAdmin</b> to log in <a href=\"http://localhost:9060/decisioncenter\">Operation Decision Manager</a>. Source code on <a href=\"https://github.com/DecisionsDev/llm-odm/tree/imagesanalysis/chat-with-images\">github</a>.")
    file_msg = btn.click(add_file, [chatbot, btn_img], [chatbot], queue=False).then(
        bot, chatbot, chatbot)

    gallery.select(on_select_gallery_image, None, None)

#    chatbot.like(print_like_dislike, None, None)


demo.queue()
if __name__ == "__main__":
    demo.launch(allowed_paths=["./data/shop"], server_name="0.0.0.0",show_api=False,favicon_path=(os.path.join(os.path.dirname(__file__), "avatar.png")))

