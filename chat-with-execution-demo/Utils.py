  
@staticmethod
def extractRulesTraceInformations(props):
    link=''
    name=''
    for prop in  props:
        if prop['name'] == 'ilog.rules.teamserver.elementID':
            # Extraire et afficher la valeur de 'value' pour cette propriété
            link="http://localhost:9060/decisioncenter/t/library#overviewbranch?baselineId=brm.Branch:16:16&id="+prop['value']
        if prop['name'] == 'ruleExecutionShortName':
            # Extraire et afficher la valeur de 'value' pour cette propriété
            name=prop['value']

    return name,link

@staticmethod
def format_to_markdown(data):
    markdown_text = ""
    # friendlyName={
    #               "tailoredProductNames":"Shop",
    #               "tailoredMessaging":"Recommandations ",
    #               "tailoredProducts":"Product suggestion",
    #               "tailoredChannels":"Channel",
    #               "discount":"Discount"
    #               }
    # for key, items in data['adProposal'].items():
    #     title=  friendlyName.get(key, key)  # Utilise la clé elle-même comme titre par défaut
    #     if hasattr(items, "__len__") and len(items) != 0:
    #         # Ajout de chaque élément de la liste comme point de puce
    #         markdown_text += f"### {title}\n"
    #         for item in items:
    #             if(key == "tailoredProductNames"):
    #                 item="<img src=\"file/data/shop/"+item+"\"/>"
    #                 markdown_text += f"{item}\n"
    #             else: 
    #                 markdown_text += f"- {item}\n"
    #         # Ajout d'un saut de ligne entre les sections pour une meilleure lisibilité
    #         markdown_text += "\n"
    #     else:
    #         if(key == "discount") and items > 0.0:                 
    #             title=  friendlyName.get(key, key)  # Utilise la clé elle-même comme titre par défaut
    #             markdown_text += f"### **{title} : <span style=\"color:blue\">{items} %</span>**"


    # To Retrieve the content of the rules : http://localhost:9060/decisioncenter-api/v1/projects/f4440cab-4dca-471c-8a9e-ec05ede7c031/rules?withContent=true

    markdown_text +=f"\n**Rules triggered :**"
    for item in data['__decisionTrace__']['rulesFired']['ruleInformation']:
        name, link = extractRulesTraceInformations(item['properties']['property'])
        markdown_text +=f" ["+name+"]("+link+")&nbsp; ,  "
    return markdown_text
@staticmethod
def formatDecisionResponse(message):
    if "error" in message:
        return message['error']
    return format_to_markdown(message)
