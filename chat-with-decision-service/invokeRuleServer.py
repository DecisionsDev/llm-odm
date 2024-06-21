import requests
from requests.auth import HTTPBasicAuth
import logging
import json
import os 
class InvokeRuleServer:
    def __init__(self):

        # Données à envoyer dans le payload de la requête POST
        self.payload =   {
         
        }
        self.trace={ 
            "__TraceFilter__": {
                "none": True,
                "infoTotalRulesFired": True,
                "infoRulesFired": True
                }
            }
        # Informations d'authentification
        self.username = 'odmAdmin'
        self.password = 'odmAdmin'
       
        self.odm_server_url =  os.getenv("ODM_SERVER_URL","http://localhost:9060")
        self.checkODMServer()
        
    def invokeRules(self,extractedPictureElements):
        # Effectuer la requête POST avec authentification Basic
        rulesetPath="/mydeployment/Miniloan_ServiceRuleset"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        params = {**extractedPictureElements, **self.trace}

        try:
            print("URL : "+self.odm_server_url+'/DecisionService/rest'+rulesetPath)

            response = requests.post(self.odm_server_url+'/DecisionService/rest'+rulesetPath, headers=headers,
                                    json=params, auth=HTTPBasicAuth(self.username, self.password))

            # Vérifier la réponse
            if response.status_code == 200:
                return response.json()
                #return "```\n"+str(json.dumps(response.json(), indent=2))+"\n```"
            else:
                print(f"Erreur de requête, code de statut: {response.status_code}")
        except requests.exceptions.RequestException as e:  # Cette ligne capture les erreurs liées aux requêtes
            return {"error": "An error occured when inovking the Decision Service. "}
    


    def checkODMServer(self):
        # Effectuer la requête POST avec authentification Basic
        # /api/v1/ruleapps
        response = requests.get(self.odm_server_url+"/res/api/v1/ruleapps", json=self.payload, auth=HTTPBasicAuth(self.username, self.password))

        # Vérifier la réponse
        if response.status_code != 200:
            print(f"Unable de context Decision Server console, code de statut: {response.status_code}")
            exit(1)

        response = requests.get(self.odm_server_url+"/DecisionService", json=self.payload, auth=HTTPBasicAuth(self.username, self.password))

        # Vérifier la réponse
        if response.status_code != 200:
            print(f"Unable de context Decision Server Runtime , code de statut: {response.status_code}")
        else:
            print(f"Connection with ODM Server is OK")

