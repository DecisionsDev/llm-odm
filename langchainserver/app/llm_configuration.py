import json
import os
from enum import Enum
from pydantic import BaseModel
class ModelConfiguration(str, Enum):
    ollama = "ollama"
    watsonx = "watsonx"
    OpenAI = "openai"

class ServerConfig(BaseModel):
    def to_dict(self):
        return {
            "name": self.name,
            "username": self.username,
            "api_key": self.api_key,
            "url": self.url,
            "model_name": self.model_name,
            "type": self.model_type.value
        }
    name: str 
    username: str 
    api_key: str
    url: str 
    model_name: str | None = ""
    model_type: ModelConfiguration 

class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ServerConfigManager:
    def __init__(self, filepath):
        self.filepath = filepath


    def load_configs(self):
       # Vérifier si le fichier existe
        if not os.path.exists(self.filepath):
            self.configs = []
            self.save_configs()  # Créer un nouveau fichier JSON vide
            return

        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                print(data)
                self.configs = [ServerConfig(**config) for config in data["ServerConfig"]]
        except  Exception as e:
            # Gérer l'erreur en cas de problème avec le fichier
            print(f"Erreur lors du chargement du fichier JSON. Création d'un nouveau fichier vide. :  {e}")
            self.configs = []
            self.save_configs()

    def update_config(self, newConfig):
            # Trouver la configuration par le nom
            for config in self.configs:
                if config.name == newConfig.name:
                    # Mettre à jour les attributs si de nouvelles valeurs sont fournies
                    if newConfig.username is not None:
                        config.username = newConfig.username
                    if newConfig.api_key is not None:
                        config.api_key = newConfig.api_key
                    if newConfig.url is not None:
                        config.url = newConfig.url
                    if newConfig.model_name is not None:
                        config.model_name = newConfig.model_name
                    if newConfig.model_type is not None:
                        print("Type"+str(newConfig.model_type))
                        config.model_type = newConfig.model_type
                    return True  # Retourner True si la mise à jour a réussi
            return False  # Retourner False si aucune configuration correspondante n'a été trouvée
    def get_configs(self):
            return self.configs
    
    def get_config_by_name(self, name):
        for config in self.configs:
            if config.name == name:
                return config
        raise ConfigError(f"Config with the name '{name}' was not found.")
    
    def save_configs(self):
        try:
            with open(self.filepath, 'w') as file:
                data = {"ServerConfig": [config.to_dict() for config in self.configs]}
                json.dump(data, file, indent=4)
            print("Configurations successfully saved.")
        except Exception as e:
            print(f"An error occured during when saving the configuration. : {e}")


    def add_config(self, config):
        self.configs.append(config)
